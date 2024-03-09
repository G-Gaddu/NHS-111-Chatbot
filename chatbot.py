# Import gradio to build the UI

import gradio as gr

# Import data

from Breathing_Problems_Data import build_data_tree, get_options
data_tree = build_data_tree()

# Import prompt and GPT's response
from prompt_completion import get_prompt, get_completion

# Function for asking GPT to predict user's response to a question
# Return the next node/question based on GPT response, or if GPT is unsure return the string 'more_info_required'
def ask_question(message, all_messages, source_node):
    options, targets = get_options_and_targets(data_tree, source_node)
    if options == []:
        return "no_options"
    else:
        question = data_tree.nodes[source_node]['text']
        prompt = get_prompt(message, all_messages, question, options)
        print(prompt)
        system_message = f"You are a helpful chatbot who understands symptoms of breathing problems that lead to high blood pressure"
        response = get_completion([{"role": "system", "content": system_message},{"role": "user", "content": prompt}])
        print(response["choices"][0]["message"]["content"])
        if "more information is required".lower() in response ["choices"][0]["message"]["content"].lower():
            return "more_info_required"
        else:
            for i in range(len(options)):
                if options[i].lower() in response["choices"][0]["message"]["content"].lower():
                    return(options[i],targets[i])
                
# Chatbot logic
source_node = 'level10_Q1'
all_messages = []
def respond(message, chat, history):
    global source_node
    global all_messages
    while True:
        try:
            answer = ask_question(message, all_messages, source_node)
            if answer:
                if answer == "more_info_required":
                    bot_message = data_tree.node[source_node]['text']
                    all_messages.append((message, bot_message))
                    print("Not enough info", bot_message)
                    break
                elif answer == "no_options" :
                    bot_message = data_tree.nodes[source_node]['text']
                    print("Outcome:", bot_message)
                    source_node = 'level10_Q1'
                    all_messages = []
                    break
                else:
                    option, target = answer
                    print("Question skipped", data_tree.nodes[source_node]['text'], "Answer:", option)
                    source_node = target
            else:
                bot_message = "An error occurred. Please try again later."
                break
        except:
            bot_message = "An error occurred. Please try again later."
            break
    chat_history.append((message, bot_message)
    return "", chat_history

# Build UI
with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    msg = gr.Textbox(label="Type a message")
    btn = gr.Button("Send")
    clear = gr.ClearButton(components=[msg, chatbot], value = "Clear chat")
    
    btn.click(respond, inputs=[msg, chatbot], outputs=[msg, chatbots])
    msg.submit(respond, inputs=[msg, chatbot], outputs=[msg, chatbot])
gr.close_all()
demo.launch()

    
                
                    
                                   
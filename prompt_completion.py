import os
import openai
from dotenv import load_dotenv, find_dotenv

# Set API key
os.environ['OPEN_API_KEY'] = # INSERT KEY HERE ''
_ = load_dotenv(find_dotenv())

open.api_key = os.getenv('OPEN_API_KEY')

# Helper function to get response from OpenAI API
def get_completion(message, model="gpt-4"):
    response = openAI.ChatCompletion.create(
        model = model,
        messages = messages,
        temperature = 0)
    return response

user_delimiter = "###"
# Function to get the conversation between the user and the chatbot
def get_conversation(message, all_messages):
    conversation = ""
    for turn in all messages:
        user_message, bot_message = turn
        conversation = f"{conversation}\nUser: {user_delimiter}{user_message}{user_delimiter}\nDoctor: {bot_message}"
    conversation = f"{conversation}\nUser: {user_delimiter}{message}{user_delimiter}\nDoctor:"
    return conversation

# Prompt sent to GPT as we traverse the questions
def get_prompt(message, all_messages, question, options):
    prompt = f""" Consider the following conversations between a user and a doctor.\
    The user starts by describing how they feel. The doctor asks the user a follow up question. \
    The user replies to the quesiont with a response delimited with {user_delimiter} characters. \
    The conversation continues in the same way. \
    f"{get_conversation(message, all_message)} {question}\nUser:"\
    Among the options listted below, what will the user select as an answer to the doctor's latest questions?
    Options: {options}
    You should think step by step and consider everything the user says in the entire conversations
    Explain your thinking
    If there is not enough information to determine what the user will select, answer with "more information required
    """
    return prompt
    

import os
import time
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import AIMessage, HumanMessage
from ca_vntl_helper import error_tracking_decorator

from api.models import Conversation, SystemPrompt

# Function to convert a chat string to a message object to store in the chat history
def convert_chat_dict_to_prompt(dict_message):
    if dict_message['message_type'] == 'human_message':
        return HumanMessage(dict_message['content'])
    if dict_message['message_type'] == 'ai_message':
        return AIMessage(dict_message['content'])
    else:
        raise ValueError("Invalid type")

# Initialize the LLM model
def load_llm(llm_provider):
    if llm_provider == 'google':
        return ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=os.getenv("GOOGLE_API_KEY"))
    elif llm_provider == 'open_ai':
        return ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=os.getenv("OPENAI_API_KEY"))    
    elif llm_provider == 'anyscale':
        pass
    elif llm_provider == 'local':
        # ollama, llm studio
        pass

def get_expert_prompt(expert_name):
    print('get expert prompt here')
    #load model instance sq by filter
    system_prompt_qs = SystemPrompt.objects.filter(expert_name=expert_name)
    if not system_prompt_qs.exists():
        raise Exception("System Prompt not found")
    
    system_prompt_instance = system_prompt_qs.first()
    system_prompt = system_prompt_instance.prompt

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}")
    ])

    return prompt

def run_chatbot(input_text, chat_history, expert_name='friend', llm_provider='google'):
    # load llm
    llm = load_llm(llm_provider)

    # select prompt and expert 
    prompt = get_expert_prompt(expert_name)

    # init chain
    output_parser = StrOutputParser()
    chain = prompt | llm | output_parser
    output = chain.invoke({"input": input_text, "chat_history": chat_history})

    return output

@error_tracking_decorator
def get_message_from_chatbot(conversation_id, user_message):
    # user_input = user_message
    # chat_history
    # expert
    # provider
    # ===========> conversation_model
    print('dajkdakakjda')
    conversation_instance_qs = Conversation.objects.filter(user_id=conversation_id)
    if not conversation_instance_qs.exists():
        raise Exception("Conversation not found")
    conversation_instance = conversation_instance_qs.first()

    expert = conversation_instance.expert_name
    provider = conversation_instance.gpt_model
    chat_history_dicts = conversation_instance.chat_history

    chat_history = [convert_chat_dict_to_prompt(chat_history_dict) for chat_history_dict in chat_history_dicts]

    response = run_chatbot(user_message, chat_history, expert, provider)

    conversation_instance.chat_history.append({"message_type": "human_message", "content": user_message})
    conversation_instance.chat_history.append({"message_type": "ai_message", "content": response})

    conversation_instance.save()

    return response
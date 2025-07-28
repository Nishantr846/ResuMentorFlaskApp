from langchain_community.llms import Ollama
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
import os
from dotenv import load_dotenv

load_dotenv()

def get_llm():
    callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
    
    llm = Ollama(
        model="mistral",
        callback_manager=callback_manager,
        temperature=0.7,
        timeout=60
    )
    return llm

def call_llm(prompt, system_prompt="You are a helpful AI assistant."):
    try:
        llm = get_llm()
        formatted_prompt = f"System: {system_prompt}\n\nUser: {prompt}\n\nAssistant:"
        response = llm.invoke(formatted_prompt)
        return response.strip()
    except Exception as e:
        return f"Error calling LLM: {str(e)}"
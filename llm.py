import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load the API key from the .env file
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Configure the model
model = genai.GenerativeModel('gemini-1.5-flash')

def call_llm(prompt):
    """
    Calls the Google Gemini API with the given prompt.
    """
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Error calling Google AI: {e}")
        return f"Error: The AI model could not be reached. Please check the server logs."
import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Debugging: Check if API key is loaded correctly
api_key = os.getenv("OPENAI_API_KEY")
print(f"API Key: {api_key}")  # This should print your API key or None if not loaded

# If the key is loaded correctly, proceed with setting it in OpenAI
import openai
if api_key:
    openai.api_key = api_key
    print("OpenAI API Initialized")
else:
    print("API key is missing! Please check the .env file.")
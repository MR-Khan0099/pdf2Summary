import os
from dotenv import load_dotenv

load_dotenv()

# Set your OpenAI API key
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY",'')
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import OpenAI API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
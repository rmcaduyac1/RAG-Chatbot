import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import Pinecone API Key
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
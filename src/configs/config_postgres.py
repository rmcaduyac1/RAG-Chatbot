import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import PostgreSQL connection string
DB_URL_CHATBOT = os.getenv("DB_URL_CHATBOT")
DB_URL_CHAINLIT = os.getenv("DB_URL_CHAINLIT")

connection_kwargs = {"autocommit": True, "prepare_threshold": 0}

if __name__ == "__main__":
    print("DB_URL_CHATBOT:", DB_URL_CHATBOT)
    print("DB_URL_CHAINLIT:", DB_URL_CHAINLIT)
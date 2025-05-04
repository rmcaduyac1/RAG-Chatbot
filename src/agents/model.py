# Import necessary libraries
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

# Initialize the chatbot model
def init_chatbot_model(model: str):
    return ChatOpenAI(model = model)

# Initialize vector embedding
def init_embed_model(model: str):
    return OpenAIEmbeddings(model = model)
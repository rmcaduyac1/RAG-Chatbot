# Import necessary libraries
import os
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone
from agents.model import init_embed_model

# Load environment variables
load_dotenv()
os.environ["PINECONE_API_KEY"] = os.getenv("PINECONE_API_KEY")

# Define tools
def retriever_tools():

    # Define vector embeddings
    embeddings = init_embed_model("text-embedding-3-small")

    # Define vector store for medicine and hazard book
    pc = Pinecone()
    index_medicine = pc.Index("medicine-book")
    index_hazard = pc.Index("hazard")
    vector_store_medicine = PineconeVectorStore(embedding = embeddings, index = index_medicine)
    vector_store_hazard = PineconeVectorStore(embedding = embeddings, index = index_hazard)
    
    # For medicine information retrieval
    @tool
    def medicine_info_retrieval(query: str) -> str:
        """
        Use this tool only if the question asks about general medicine concepts.
        """
        
        batch_results = vector_store_medicine.similarity_search(query, k = 2)
        serialized = "\n\n".join(
            (f"Content: {batch.page_content}") for batch in batch_results
        )
        
        return serialized
    
    # For hazard, medical and solid waste information retrieval
    @tool
    def hazard_med_solid_waste_info_retrieval(query: str) -> str:
        """
        Use this tool only if the question asks about general hazardous, medical, and solid waste concepts.
        """
        
        batch_results = vector_store_hazard.similarity_search(query, k = 2)
        serialized = "\n\n".join(
            (f"Content: {batch.page_content}") for batch in batch_results
        )
        
        return serialized
    
    # Get all function tools
    all_tools = [
        medicine_info_retrieval,
        hazard_med_solid_waste_info_retrieval
    ]

    return all_tools


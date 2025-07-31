# Import necessary libraries
import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone

# Load environment variables
load_dotenv()
os.environ["PINECONE_API_KEY"] = os.getenv("PINECONE_API_KEY")
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# Load the PDF files
loader_medicine = PyPDFLoader("src/data/medicine.pdf")
loader_hazard = PyPDFLoader("src/data/hazardous-medical-solid_waste.pdf")

# Retrieve the PDF files
medicine_doc = loader_medicine.load()
hazard_doc = loader_hazard.load()

# Split the documents
text_splitter = RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap = 200, add_start_index = True)
medicine_splits = text_splitter.split_documents(medicine_doc)
hazard_splits = text_splitter.split_documents(hazard_doc)

# Define vector embeddings
embeddings = OpenAIEmbeddings(model = "text-embedding-3-small")

# Store to pinecone vectorstore
pc = Pinecone()
index_medicine = pc.Index("medicine-book")
index_hazard = pc.Index("hazard")
vector_store_medicine = PineconeVectorStore(embedding = embeddings, index = index_medicine)
vector_store_hazard = PineconeVectorStore(embedding = embeddings, index = index_hazard)

# Process documents in batches to avoid OpenAI token limits
def add_documents_in_batches(vector_store, documents, batch_size=1500):
    all_ids = []
    i = 0
    while i < len(documents):
        batch = documents[i:i + batch_size]
        print(f"Processing batch {i//batch_size + 1} ({len(batch)} documents)")
        
        try:
            batch_ids = vector_store.add_documents(documents = batch)
            all_ids.extend(batch_ids)
            i += batch_size
        except Exception as e:
            if "max_tokens_per_request" in str(e):
                print(f"Batch too large, retrying with smaller size...")
                # Retry with half the batch size
                half_batch = documents[i:i + batch_size//2]
                batch_ids = vector_store.add_documents(documents = half_batch)
                all_ids.extend(batch_ids)
                i += batch_size//2
            else:
                raise e
    return all_ids

print(f"Processing {len(medicine_splits)} medicine documents...")
ids_medicine = add_documents_in_batches(vector_store_medicine, medicine_splits)

print(f"Processing {len(hazard_splits)} hazard documents...")
ids_hazard = add_documents_in_batches(vector_store_hazard, hazard_splits)
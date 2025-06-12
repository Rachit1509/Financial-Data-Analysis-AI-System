# vector.py

from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
import os
import pandas as pd

# Load financial data from CSV
df = pd.read_csv("financial_data.csv")  # Make sure this file is present

# Use Ollama embeddings
embeddings = OllamaEmbeddings(model="mxbai-embed-large")

# Set up Chroma vector DB
db_location = "./chroma_finance_db"
add_documents = not os.path.exists(db_location)

if add_documents:
    documents = []
    ids = []

    for i, row in df.iterrows():
        content = f"Date: {row['Date']}, Category: {row['Category']}, Description: {row['Description']}, Amount: ₹{row['Amount (INR)']}, Type: {row['Type']}"
        document = Document(
            page_content=content,
            metadata={"category": row["Category"], "type": row["Type"]},
            id=str(i)
        )
        documents.append(document)
        ids.append(str(i))

# Create or load vector store
vector_store = Chroma(
    collection_name="financial_records",
    persist_directory=db_location,
    embedding_function=embeddings
)

# Add documents to DB if first run
if add_documents:
    vector_store.add_documents(documents=documents, ids=ids)

# Create retriever
retriever = vector_store.as_retriever(
    search_kwargs={"k": 5}
)

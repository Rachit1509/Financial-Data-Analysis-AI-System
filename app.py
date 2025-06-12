# app.py

from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
import pandas as pd
import os

from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

app = FastAPI()

# Initialize LLM and prompt template
model = OllamaLLM(model="llama3.2")
prompt = ChatPromptTemplate.from_template("""
You are a financial assistant. Use the following financial records to answer user questions.

Data snippets:
{data}

User's question:
{question}
""")

retriever = None  # global retriever




@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        # Create a safe uploads directory
        UPLOAD_DIR = "uploads"
        os.makedirs(UPLOAD_DIR, exist_ok=True)

        # Save uploaded file to uploads/
        contents = await file.read()
        temp_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(temp_path, "wb") as f:
            f.write(contents)

        # Proceed with processing
        df = pd.read_csv(temp_path)

        # Create documents for vector DB
        documents = []
        ids = []

        for i, row in df.iterrows():
            content = f"Date: {row['Date']}, Category: {row['Category']}, Description: {row['Description']}, Amount: ₹{row['Amount (INR)']}, Type: {row['Type']}"
            doc = Document(
                page_content=content,
                metadata={"category": row["Category"], "type": row["Type"]},
                id=str(i)
            )
            documents.append(doc)
            ids.append(str(i))

        # Create vector store
        db_path = "./chroma_finance_db_api"
        if os.path.exists(db_path):
            import shutil
            shutil.rmtree(db_path)

        embeddings = OllamaEmbeddings(model="mxbai-embed-large")
        vector_store = Chroma(
            collection_name="financial_api_data",
            persist_directory=db_path,
            embedding_function=embeddings
        )
        vector_store.add_documents(documents=documents, ids=ids)

        global retriever
        retriever = vector_store.as_retriever(search_kwargs={"k": 5})

        return {"message": "File uploaded and vector store initialized."}
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})

@app.post("/query")
async def query(question: str = Form(...)):
    if not retriever:
        return JSONResponse(status_code=400, content={"error": "Please upload a financial data file first."})

    try:
        docs = retriever.invoke(question)
        data = "\n".join([doc.page_content for doc in docs])
        chain = prompt | model
        result = chain.invoke({"data": data, "question": question})
        return {"response": result}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

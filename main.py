# main.py

from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from vector import retriever

# Initialize the model
model = OllamaLLM(model="llama3.2")

# Updated prompt template for financial insights
template = """
You are a financial assistant. Based on the provided financial records, answer the user's question.

Here are some relevant financial data snippets:
{data}

User's question:
{question}
"""

# Prepare chain
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

# Main loop for user queries
while True:
    print("\n\n-------------------------------")
    question = input("Ask your financial question (q to quit): ")
    print("\n\n")
    if question.lower() == "q":
        break

    docs = retriever.invoke(question)
    data = "\n".join([doc.page_content for doc in docs])
    
    result = chain.invoke({"data": data, "question": question})
    print("🔍 Response:")
    print(result)

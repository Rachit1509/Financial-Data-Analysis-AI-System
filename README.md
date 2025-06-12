# Financial Data Analysis AI-System

A FastAPI-based application that processes financial data and enables natural language queries using LangChain, Ollama, and ChromaDB for vector storage.

## Features

- File upload endpoint for financial data (CSV format)
- Vector database storage using ChromaDB
- Natural language query processing using Ollama LLM
- Financial data analysis capabilities
- RESTful API endpoints

## Tech Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **LangChain**: Framework for developing applications powered by language models
- **Ollama**: Local large language model integration
- **ChromaDB**: Vector database for storing and retrieving embeddings
- **Pandas**: Data manipulation and analysis
- **Python 3.12**: Core programming language

## Project Structure

```
├── app.py              # Main FastAPI application
├── vector.py           # Vector database operations
├── financial_data.csv  # Sample financial data
├── requirements.txt    # Project dependencies
└── uploads/           # Directory for uploaded files
    └── financial_data.csv
```

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd VCS_TASK
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
.\venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Make sure Ollama is installed and running on your system with the required models:
- llama3.2
- mxbai-embed-large

## Usage

1. Start the FastAPI server:
```bash
uvicorn app:app --reload
```

2. The API will be available at `http://localhost:8000`

3. Use the following endpoints:
- POST `/upload`: Upload financial data (CSV format)
- Additional endpoints as per application requirements

4. Access the API Interface via Swagger UI
    Open your browser and go to:

    http://localhost:8000/docs

    There, you can:
    Upload your financial CSV file using the /upload endpoint.
    Ask questions using the /query endpoint.

5. Sample Questions to Try:

    "What are the top 5 expenses this month?"

    "Summarize expenses by category."

    "How much did I spend on groceries in June?"

## File Format

The application expects CSV files with the following columns:
- Date
- Category
- Description
- Amount (INR)
- Type

## Dependencies

See `requirements.txt` for a complete list of dependencies:
- fastapi
- uvicorn
- langchain
- langchain-ollama
- langchain-chroma
- pandas
- openpyxl
- python-multipart




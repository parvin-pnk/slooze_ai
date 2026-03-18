# AI Agent: Web Search & PDF RAG System

A multi-modal AI Agent built using FastAPI that combines real-time web search and document-based RAG.

# Features

AI Web Search Agent
  -Real-time search using Tavily API
  -results using LLM

PDF RAG System

  -upload and process PDFs
  -Semantic search using FAISS
  -Context-aware question answering


Web Search Flow

1. User Query
2. Tavily API Search
3. Extract relevant results
4. Pass context to LLM
5. Generate synthesized answer

PDF RAG Pipeline

1. PDF Upload → Text Extraction
2. Text Chunking (semantic splitting)
3. Embedding Generation (all-MiniLM-L6-v2)
4. Vector Storage (FAISS Index)
5. Query → Embedding
6. Top-K Similarity Search
7. Context Injection into LLM
8. Final Answer Generation


Tech Stack

- Framework: FastAPI (Python)
- LLM Provider: OpenRouter (NVIDIA Nemotron 120B)
- Search Tool: Tavily API
- Vector Store: FAISS
- Embeddings: Sentence-Transformers (all-MiniLM-L6-v2)


Installation & Setup

1. Clone Repository

    git clone <your-repo-url>
    cd slooze_ai

2. Create Virtual Environment

    python -m venv venv
    venv\Scripts\activate

3. Install Dependencies

    pip install -r requirements.txt


Running the Application

    python main.py
    or
    uvicorn main:app --reload --port 8000

* API: http://127.0.0.1:8000
* Swagger Docs: http://127.0.0.1:8000/docs


API Endpoints

Web Search

POST /search/

Request:
{
  "query": "Latest specs of MacBook Pro 2026"
}

Response:
* Synthesized answer
* Source URLs


PDF RAG

Upload PDF

POST /pdf/process

* Input: `multipart/form-data`
* Key: `file`

Response:

{
  "file_id": "uuid"
}



Query PDF

POST /pdf/query


{
  "file_id": "uuid",
  "question": "What is the methodology?"
}


Response:

* Context-aware answer from document




Testing

python check_llm.py      # Verify LLM connectivity
python check_tavily.py  # Verify search API



Conclusion

This project demonstrates a **real-world AI system design**, combining:

* Retrieval (FAISS)
* External tools (Tavily)
* LLM reasoning (Nemotron 120B)


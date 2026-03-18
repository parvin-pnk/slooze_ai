import os
import io
import uuid
import numpy as np
import faiss
from pypdf import PdfReader
from fastapi import UploadFile
from sentence_transformers import SentenceTransformer
from common.llm_client import get_llm_response


embed_model = SentenceTransformer('all-MiniLM-L6-v2')

vector_indices = {}
text_chunks_storage = {}

def chunk_text(text, chunk_size=1000, overlap=100):
    chunks = []
    for i in range(0, len(text), chunk_size - overlap):
        chunks.append(text[i:i + chunk_size])
    return chunks

async def ingest_pdf_with_faiss(file: UploadFile):

    content = await file.read()
    pdf_stream = io.BytesIO(content)
    
    try:
        reader = PdfReader(pdf_stream)
        full_text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                full_text += page_text + "\n"
        
        if not full_text.strip():
            return None

        file_id = str(uuid.uuid4())
        chunks = chunk_text(full_text)
        embeddings = embed_model.encode(chunks)
        
        dimension = embeddings.shape[1]
        index = faiss.IndexFlatL2(dimension)
        index.add(np.array(embeddings).astype('float32'))
        
        vector_indices[file_id] = index
        text_chunks_storage[file_id] = chunks
        
        return file_id
    except Exception as e:
        print(f"Ingestion Error: {e}")
        return None

def query_pdf_with_faiss(file_id: str, question: str):
    index = vector_indices.get(file_id)
    chunks = text_chunks_storage.get(file_id)
    
    if not index or not chunks:
        return "Error: Document context not found. please upload the PDF again."

    question_embedding = embed_model.encode([question])
    distances, indices = index.search(np.array(question_embedding).astype('float32'), k=3)

    retrieved_context = ""
    for idx in indices[0]:
        if idx != -1:
            retrieved_context += chunks[idx] + "\n---\n"

    prompt = f"""
    You are an expert analyst. Answer the question based ONLY on the following document context.
    
    Context:
    {retrieved_context}
    
    Question: {question}
    """
    
    return get_llm_response(prompt)
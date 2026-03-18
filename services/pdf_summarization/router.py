from fastapi import APIRouter, UploadFile, File, HTTPException
from .schema import PDFQueryRequest
from .services import ingest_pdf_with_faiss, query_pdf_with_faiss

router = APIRouter(prefix="/pdf", tags=["PDF Analysis"])

@router.post("/process")
async def process_pdf(file: UploadFile = File(...)):
    file_id = await ingest_pdf_with_faiss(file)
    if not file_id:
        raise HTTPException(status_code=500, detail="Failed to process PDF")
    return {"message": "Success", "file_id": file_id}

@router.post("/query")
async def query_pdf(payload: PDFQueryRequest):
    answer = query_pdf_with_faiss(payload.file_id, payload.question)
    return {"answer": answer}
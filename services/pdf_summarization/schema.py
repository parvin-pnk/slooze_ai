from pydantic import BaseModel
from typing import Optional

class PDFProcessRequest(BaseModel):
    file_path: str

class PDFQueryRequest(BaseModel):
    file_id: str
    question: str
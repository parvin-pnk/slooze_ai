from pydantic import BaseModel
from typing import List

class SearchQuery(BaseModel):
    query: str

class SearchResponse(BaseModel):
    answer: str
    sources: List[str]
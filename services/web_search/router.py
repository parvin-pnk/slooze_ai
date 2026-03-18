from fastapi import APIRouter, HTTPException
from .schema import SearchQuery, SearchResponse
from .services import perform_web_search_and_summarize

router = APIRouter(prefix="/search", tags=["Web Search"])

@router.post("/", response_model=SearchResponse)
async def web_search(payload: SearchQuery):
    try:
        answer, sources = perform_web_search_and_summarize(payload.query)
        return SearchResponse(answer=answer, sources=sources)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
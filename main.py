from fastapi import FastAPI
from services.web_search.router import router as search_router
from services.pdf_summarization.router import router as pdf_router

app = FastAPI(title="AI Agent API")


app.include_router(search_router)
app.include_router(pdf_router)

@app.get("/")
async def root():
    return {"message": "AI Agent System is Online"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, timeout_keep_alive=75)
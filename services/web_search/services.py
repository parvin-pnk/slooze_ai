import os
import requests
from common.llm_client import get_llm_response

def perform_web_search_and_summarize(query: str):
    api_key = os.getenv("TAVILY_API_KEY")
    url = "https://api.tavily.com/search"
    
    payload = {
        "api_key": api_key,
        "query": query,
        "search_depth": "basic",
        "max_results": 3
    }

    results = []
    sources = []

    try:
        response = requests.post(url, json=payload, timeout=15)
        
        if response.status_code != 200:
            return f"Search API Error: Received status {response.status_code}", []

        data = response.json()
        results = data.get("results", [])

    except Exception as e:
        return f"System Connection Error: {str(e)}", []

    if not results:
        return "I couldn't find any information on topic.", []
    
    context_parts = []
    for r in results:
       
        if isinstance(r, dict):
            content = r.get("content", "No content available.")
            url_link = r.get("url", "No source link.")
            context_parts.append(f"Source: {url_link}\nContent: {content}")
            sources.append(url_link)

    context_text = "\n\n".join(context_parts)

    prompt = f"""
    You are a real-time AI assistant. Based on the search results below, 
    provide a helpful answer to the user's question.
    
    User Question: {query}
    
    Search Results:
    {context_text}
    
    Answer:
    """
    
    try:
        answer = get_llm_response(prompt)
    except Exception as e:
        answer = f"Error generating LLM response: {str(e)}"

    return answer, sources
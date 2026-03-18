import os
import requests
import json
from dotenv import load_dotenv


load_dotenv()
api_key = os.getenv("TAVILY_API_KEY")

def test_tavily_search():
    print("--- Testing Tavily Search (API Check) ---")
    
    if not api_key:
        print("ERROR: TAVILY_API_KEY not found in your .env file.")
        return


    url = "https://api.tavily.com/search"
    
    payload = {
        "api_key": api_key,
        "query": "Latest AI news March 2026",
        "search_depth": "basic",
        "max_results": 3
    }

    try:
        print(f"Action: Sending request to Tavily...")
        response = requests.post(url, json=payload, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            results = data.get("results", [])
            
            if results:
                print(f"SUCCESS: Found {len(results)} results.")
                print(f"Top Title: {results[0]['title']}")
                print(f"Top URL: {results[0]['url']}")
            else:
                print("FAILED: API responded successfully but returned 0 results.")
                
        elif response.status_code == 401:
            print("FAILED: Unauthorized (401). Your API Key is likely invalid.")
        elif response.status_code == 429:
            print("FAILED: Rate Limit (429). You have run out of free credits.")
        else:
            print(f"FAILED: Status Code {response.status_code}")
            print(f"Response Body: {response.text}")

    except Exception as e:
        print(f"ERROR: {str(e)}")

if __name__ == "__main__":
    test_tavily_search()
import os
import time
from common.llm_client import get_llm_response, client
from dotenv import load_dotenv

load_dotenv()

def verify_llm_connection():
    print("--- LLM Status Check ---")
    print(f"Base URL: {client.base_url}")
    print(f"Model: openrouter/nvidia/nemotron-3-super-120b-a12b:free")
    print("-" * 25)

    test_prompt = "Respond with the word 'Online' and nothing else."
    
    start_time = time.time()
    try:
        response = get_llm_response(test_prompt)
        
        end_time = time.time()
        latency = end_time - start_time

        if "Online" in response:
            print(f"STATUS: [SUCCESS]")
            print(f"Response: {response.strip()}")
            print(f"Latency: {latency:.2f} seconds")
        else:
            print(f"STATUS: [PARTIAL SUCCESS]")
            print(f"Unexpected Response: {response}")
            
    except Exception as e:
        print(f"STATUS: [FAILED]")
        print(f"Error Detail: {str(e)}")
        
        if "401" in str(e):
            print("Check: Your OPENROUTER_API_KEY might be invalid.")
        elif "timeout" in str(e).lower():
            print("Check: The server is taking too long. The model might be overloaded.")

if __name__ == "__main__":
    if not os.getenv("OPENROUTER_API_KEY"):
        print("Error: OPENROUTER_API_KEY not found in .env file.")
    else:
        verify_llm_connection()
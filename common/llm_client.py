import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=os.getenv("OPENROUTER_API_KEY"),
)

def get_llm_response(prompt: str):
    try:
        response = client.chat.completions.create(
            model="nvidia/nemotron-3-super-120b-a12b:free",
            messages=[{"role": "user", "content": prompt}],
            extra_body={"reasoning": {"enabled": True}},
            timeout=60.0  
        )

        if not response or not response.choices:
            return "Error: No response from model."

        message = response.choices[0].message
        
        if message.content:
            return message.content
        else:
            return "model thought | not final text"

    except Exception as e:
        return f"LLM Error: {str(e)}"
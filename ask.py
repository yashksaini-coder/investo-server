import groq
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")
GROQ_API_KEY = os.getenv("api_key")

groq_client = groq.Client(api_key=GROQ_API_KEY)

def chat(query: str):
    """
    API endpoint to handle user investment-related questions and return AI-generated insights.
    """
    if not query:
        return {"error": "Query parameter is required"}
    
    try:
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile", 
            messages=[{"role": "system", "content": "You are an AI investment assistant."},
                      {"role": "user", "content": query}]
        )
        
        answer = response.choices[0].message.content
        return {"question": query, "answer": answer}
    
    except Exception as e:
        return {"error": str(e)}
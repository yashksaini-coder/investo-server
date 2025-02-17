from fastapi import FastAPI
import groq
import os
from dotenv import load_dotenv

# Load API key from .env file

load_dotenv(dotenv_path=".env")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

groq_client = groq.Client(api_key=GROQ_API_KEY)

if not GROQ_API_KEY:
    raise ValueError("Please provide a GROQ API key")
    exit(1)
    
app = FastAPI()



@app.get("/ask")
def ask(query: str):
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

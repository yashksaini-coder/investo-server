import os
import datetime
import requests
import groq
from fastapi import FastAPI, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from agno.agent import RunResponse
from controllers.agents import multi_ai
import dotenv

router = APIRouter()

dotenv.load_dotenv()
templates = Jinja2Templates(directory="templates")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
groq_client = groq.Client(api_key=GROQ_API_KEY)

if not GROQ_API_KEY:
    raise ValueError("Please provide a GROQ API key")

@router.get("health/")  # Changed to GET since it's retrieving status
async def health_check():
    try:
        return {
            "status": "healthy",
            "timestamp": datetime.datetime.now().isoformat(),
            "uptime": "OK",
            "api": {
                "groq_api": "connected" if GROQ_API_KEY else "not configured",
            },
            "ip": requests.get('https://api.ipify.org').text,
            "services": {
                "top_stocks": router.url_path_for("read_top_stocks"),
                "chat": router.url_path_for("chat"),
                "agent": router.url_path_for("ask"),
            },
        }

    except Exception as e:
        return {
            "status": "unhealthy",
            "timestamp": datetime.datetime.now().isoformat(),
            "error": str(e)
        }

@router.get("/chat")
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


@router.get("/agent")
def ask(query: str):
    """
    API endpoint to handle user investment-related questions and return AI-generated insights.
    """
    if not query:
        return {"error": "Query parameter is required"}
    
    try:
        response: RunResponse = multi_ai.run(query)
        answer = response.content

        return {"question": query, "answer": answer}
    
    except Exception as e:
        return {"error": str(e)}

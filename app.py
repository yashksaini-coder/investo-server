# API imports
from fastapi import FastAPI
import groq
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from topStocks import get_top_stocks
from agents import multi_ai
from agno.agent import RunResponse
import datetime
import requests

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
groq_client = groq.Client(api_key=GROQ_API_KEY)

if not GROQ_API_KEY:
    raise ValueError("Please provide a GROQ API key")
    
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

@app.get("/top-stocks")
async def read_top_stocks():
    top_stocks = ['AAPL', 'MSFT', 'AMZN', 'GOOGL']
    stock = " ".join(top_stocks)
    stock_info = get_top_stocks(stock)
    return stock_info

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Investo-glow Backend API!"}


@app.get("health/")  # Changed to GET since it's retrieving status
async def health_check():
    try:
        return {
            "status": "healthy",
            "timestamp": datetime.datetime.now().isoformat(),
            "uptime": "OK",
            "api": {
                "groq_api": "connected" if GROQ_API_KEY else "not configured",
            },
            "ip": requests.client.host,
            "services": {
                "top_stocks": app.url_path_for("read_top_stocks"),
                "chat": app.url_path_for("chat"),
                "agent": app.url_path_for("ask"),
            },
        }

    except Exception as e:
        return {
            "status": "unhealthy",
            "timestamp": datetime.datetime.now().isoformat(),
            "error": str(e)
        }

@app.get("/chat")
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


@app.get("/agent")
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
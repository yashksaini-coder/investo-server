# API imports
from fastapi import FastAPI
import groq
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from topStocks import get_top_stocks
from agents import multi_ai
from agno.agent import RunResponse


load_dotenv(dotenv_path=".env")
GROQ_API_KEY = os.getenv("api_key")

groq_client = groq.Client(api_key=GROQ_API_KEY)

if not GROQ_API_KEY:
    raise ValueError("Please provide a GROQ API key")
    
app = FastAPI()
# Web searching agent
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

@app.get("/top-stocks")
async def read_top_stocks():
    top_stocks = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA']
    stock_info = get_top_stocks(top_stocks)
    return stock_info


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


@app.get("/ask")
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
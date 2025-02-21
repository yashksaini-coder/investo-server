# API imports
from fastapi import FastAPI, Request, Depends
import groq
import os
from dotenv import load_dotenv
import datetime
import requests

from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pyfiglet import Figlet, FigletFont
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from contextlib import asynccontextmanager
import json
from redis import asyncio as aioredis
# Custom imports
from topStocks import get_top_stocks
from agents import multi_ai
from agno.agent import RunResponse


templates = Jinja2Templates(directory="templates")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
groq_client = groq.Client(api_key=GROQ_API_KEY)

if not GROQ_API_KEY:
    raise ValueError("Please provide a GROQ API key")
REDIS_URL = os.getenv("REDIS_URL")

@asynccontextmanager
async def lifespan(_: FastAPI):
    redis_client = None  

    try:
        redis_client = aioredis.from_url(REDIS_URL, encoding="utf-8", decode_responses=True)
        FastAPICache.init(RedisBackend(redis_client), prefix="fastapi-cache")
        print("✅ Redis cache initialized successfully!")
        yield
    except Exception as e:
        print(f"❌ Redis Connection Error: {e}")
        yield 
    finally:
        try:
            await FastAPICache.clear()
            if redis_client:
                await redis_client.close()  
                print("🔴 Redis connection closed!")
        except Exception as e:
            print(f"❌ Error while closing Redis: {e}")


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

@app.get("/")
@app.head("/")
async def read_root(request: Request):
    text = "Investo-glow Backend API Server"
    return templates.TemplateResponse("base.html",{"request":request, "text": text})

def get_cache():
    return FastAPICache.get_backend()

@app.get("/top-stocks")
async def read_top_stocks(cache: RedisBackend = Depends(get_cache)):
    cache_key = "top_stocks"
    cached_result = await cache.get(cache_key)
    if cached_result:
        return json.loads(cached_result)

    top_stocks = ['AAPL', 'MSFT', 'AMZN', 'GOOGL']
    stock = " ".join(top_stocks)
    stock_info = get_top_stocks(stock)

    await cache.set(cache_key, json.dumps(stock_info), 5) 
    return stock_info

@app.get("/")
async def read_root():
    return {"Welcome to the Investo-glow Backend API!"}
    return templates.TemplateResponse("home.html",{"request": request, "home_art": home_art})

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
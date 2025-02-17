from fastapi import FastAPI
import groq
from agno.agent import Agent
from agno.models.groq import Groq
from agno.tools.yfinance import YFinanceTools
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.agent import Agent, RunResponse
import os
from dotenv import load_dotenv
# Load API key from .env file
from fastapi.middleware.cors import CORSMiddleware
from topStocks import get_top_stocks
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

web_search_agent = Agent(
    name="web_agent",
    role="search the web for information based on the user given input",
    model=Groq(id="llama-3.3-70b-specdec",api_key=GROQ_API_KEY),
    tools=[
        DuckDuckGoTools(search=True, news=True),

    ],
    instructions=[
        "You are a very professional web search AI agent",
        "your job is to search the web for information based on the user given input",
        "provide exact information to the user available on the web",
    ],
    structured_outputs=False,
    markdown=True,
)
financial_agent = Agent(
    name="financial_agent",
    role="get financial information",
    model=Groq(id="llama-3.3-70b-specdec",api_key=GROQ_API_KEY),
    tools=[
        YFinanceTools(stock_price=True,
                    analyst_recommendations=True,
                    stock_fundamentals=True, 
                    company_info=True, 
                    technical_indicators=True, 
                    historical_prices=True,
                    key_financial_ratios = True,
                    income_statements = True,
                    ),
    ],
    instructions=[
        "You are a very professional financial advisor AI agent",
        "your job is to provide financial information to users",
        "you can provide stock price, analyst recommendations, and stock fundamentals",
        "you can also provide information about companies, industries, and financial terms",
    ],
    structured_outputs=False,
    markdown=True,
)

multi_ai = Agent(
    team=[web_search_agent, financial_agent],
    model=Groq(id="llama-3.3-70b-specdec",api_key=GROQ_API_KEY),
    markdown=True,
)

@app.get("/top-stocks")
async def read_top_stocks():
    top_stocks = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA']
    stock_info = get_top_stocks(top_stocks)
    return stock_info

@app.get("/ask")
def ask(query: str):
    """
    API endpoint to handle user investment-related questions and return AI-generated insights.
    """
    if not query:
        return {"error": "Query parameter is required"}
    
    try:
        # response = financial_agent.print_response(query)
        response: RunResponse = multi_ai.run(query)
        answer = response.content

        return {"question": query, "answer": answer}
    
    except Exception as e:
        return {"error": str(e)}
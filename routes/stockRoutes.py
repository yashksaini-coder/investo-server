from fastapi import APIRouter, Depends, Request
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from utils.redisCache import get_cache
from controllers.topStocks import get_top_stocks, get_stock
from controllers.stockNews import fetch_news
from controllers.stockAgent import stock_analyzer_agent, extract_json_from_response, create_default_stock_data, merge_stock_data
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Query, HTTPException
import os
import re
import json
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")
router = APIRouter()

@router.get("/")
@router.head("/")
async def read_root(request: Request):
    text = "Investo-glow Backend API Server"
    return templates.TemplateResponse("base.html",{"request":request, "text": text})


@router.get("/top-stocks")
async def read_top_stocks(cache: RedisBackend = Depends(get_cache)):
    cache_key = "top_stocks"
    cached_result = await cache.get(cache_key)
    if cached_result:
        return json.loads(cached_result)

    top_stocks = ['AAPL', 'MSFT', 'AMZN', 'GOOGL', 'TSLA', 'META', 'NVDA']
    stocks = " ".join(top_stocks)
    stocks_info = get_top_stocks(stocks)

    await cache.set(cache_key, json.dumps(stocks_info), 10) 
    return stocks_info

@router.get("/stock-news")
async def stock_news(cache: RedisBackend = Depends(get_cache)):
    cache_key = "stock_news"
    cached_result = await cache.get(cache_key)
    if cached_result:
        return json.loads(cached_result)
    news_stack = fetch_news()
    await cache.set(cache_key, json.dumps(news_stack), 300) 
    return news_stack

@router.get("/stocks/{name}")
async def read_stock(name: str, cache: RedisBackend = Depends(get_cache)):
    # Use f-string to properly interpolate the name variable
    cache_key = f"stock_{name}"
    cached_result = await cache.get(cache_key)
    if cached_result:
        return json.loads(cached_result)
    stock_info = get_stock(name)
    await cache.set(cache_key, json.dumps(stock_info), 10)
    return stock_info



@router.get("/stock-analysis/{symbol}")
async def get_stock_analysis(symbol: str, cache: RedisBackend = Depends(get_cache)):
    cache_key = f"stock_analysis_{symbol}"
    """
    Get detailed stock analysis for a given stock symbol.
    Returns a JSON response with financial metrics.
    """
    try:
        # Construct a clear prompt for the model
        prompt = f"Analyze the stock {symbol} and provide detailed financial information following the specified JSON format."
        result = stock_analyzer_agent.run(prompt)
        
        # Extract JSON from the response
        if hasattr(result, 'content'):
            # Try to extract JSON from the content
            json_data = extract_json_from_response(result.content)
            
            if json_data:                
                # Create default data and merge with extracted data
                default_data = create_default_stock_data(symbol)
                final_data = merge_stock_data(default_data, json_data)
                
                return JSONResponse(content=final_data)
            else:
                logger.error(f"Could not extract JSON from response: {result.content[:200]}...")
        
        # Fallback to default data if extraction failed
        return JSONResponse(content=create_default_stock_data(symbol))
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Failed to retrieve stock data: {str(e)}"}
        )


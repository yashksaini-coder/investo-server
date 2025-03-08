from fastapi import APIRouter, Depends, Request
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from utils.redisCache import get_cache
from controllers.topStocks import get_top_stocks, get_stock
from controllers.stockNews import fetch_news
import json
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")
router = APIRouter()

@router.get("/top-stocks")
async def read_top_stocks(cache: RedisBackend = Depends(get_cache)):
    cache_key = "top_stocks"
    cached_result = await cache.get(cache_key)
    if cached_result:
        return json.loads(cached_result)

    top_stocks = ['AAPL', 'MSFT', 'AMZN', 'GOOGL']
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
    cache_key = "stock_{name}"
    cached_result = await cache.get(cache_key)
    if cached_result:
        return json.loads(cached_result)
    stock_info = get_stock(name)
    await cache.set(cache_key, json.dumps(stock_info), 10)
    return stock_info

@router.get("/")
@router.head("/")
async def read_root(request: Request):
    text = "Investo-glow Backend API Server"
    return templates.TemplateResponse("base.html",{"request":request, "text": text})
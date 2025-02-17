from fastapi import FastAPI
import yfinance as yf
import json
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

def get_top_stocks(symbols):
    stock_data = []
    for symbol in symbols:
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            stock_info = {
                'symbol': symbol,
                'name': info.get('shortName', 'N/A'),
                'currentPrice': info.get('currentPrice', 'N/A'),
                'previousClose': info.get('previousClose', 'N/A'),
                'sector': info.get('sector', 'N/A')
            }
            stock_data.append(stock_info)
        except Exception as e:
            print(f"Error fetching {symbol}: {e}")
    return stock_data

@app.get("/top-stocks")
async def read_top_stocks():
    top_stocks = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA']
    stock_info = get_top_stocks(top_stocks)
    return stock_info
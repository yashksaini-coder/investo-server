import yfinance as yf

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

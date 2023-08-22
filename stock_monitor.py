import requests

# Replace 'YOUR_API_TOKEN' with your actual IEX Cloud API token
API_TOKEN = 'pk_e707832aae934f04b8d2bff18da0583f'

# List of stock symbols to monitor
stock_symbols = ['TSLA', 'AAPL', 'MSFT', 'GOOGL', 'NKE']

def get_stock_prices(symbols):
    stock_prices = {}
    for symbol in symbols:
        url = f'https://cloud.iexapis.com/stable/stock/{symbol}/quote?token={API_TOKEN}'
        response = requests.get(url)
        data = response.json()
        stock_prices[symbol] = data['latestPrice']
    return stock_prices

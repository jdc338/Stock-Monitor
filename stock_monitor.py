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

# Get stock prices
stock_prices = get_stock_prices(stock_symbols)

# Print stock prices
for symbol, price in stock_prices.items():
    print(f'Current price of {symbol}: ${price}')


def get_historical_data(symbol, range='1m'):
    url = f'https://cloud.iexapis.com/stable/stock/{symbol}/chart/{range}?token={API_TOKEN}'
    response = requests.get(url)
    data = response.json()
    return data

def calculate_7_day_average(data):
    closing_prices = [entry['close'] for entry in data[-7:]]
    return sum(closing_prices) / 7

    previous_prices = {}

# Get stock prices
stock_prices = get_stock_prices(stock_symbols)

# Get 7-day moving averages
seven_day_averages = {}
for symbol in stock_symbols:
    historical_data = get_historical_data(symbol)
    seven_day_average = calculate_7_day_average(historical_data)
    seven_day_averages[symbol] = seven_day_average

def check_price_alerts(current_prices, previous_prices, threshold=0.25):
    alerts = []
    for symbol in current_prices:
        if symbol in previous_prices:
            price_diff = previous_prices[symbol] - current_prices[symbol]
            if price_diff >= threshold:
                alerts.append(symbol)
        previous_prices[symbol] = current_prices[symbol]
    return alerts

# Get current stock prices
current_prices = get_stock_prices(stock_symbols)

# Check price alerts
alerts = check_price_alerts(current_prices, previous_prices)

# Print alerts
if alerts:
    print(f"Price alerts triggered for: {', '.join(alerts)}")
else:
    print("No price alerts triggered.")

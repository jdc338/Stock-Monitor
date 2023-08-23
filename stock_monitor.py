import requests
# IEX Cloud API token
API_TOKEN = 'pk_e707832aae934f04b8d2bff18da0583f'
IFTTT_KEY = 'dPizzX0mkbuY6t15feKsoe'

# List of stock symbols to monitor
stock_symbols = ['TSLA', 'AAPL', 'MSFT', 'GOOGL', 'NKE']

def send_notification_to_ifttt(stock_alerts):
    for symbol in stock_alerts:
        url = f'https://maker.ifttt.com/trigger/stock_price_alert/with/key/{IFTTT_KEY}'
        data = {'value1': f'Alert: Price drop for {symbol}'}  # Include symbol in the value1
        response = requests.post(url, json=data)
        if response.status_code == 200:
            print(f"Notification sent for {symbol}")
        else:
            print(f"Failed to send notification for {symbol}")


def get_stock_prices(symbols):
    stock_prices = {} # Initialize an empty dictionary to store stock prices
    for symbol in symbols: # Loop through each symbol in the list 'symbols'
        url = f'https://cloud.iexapis.com/stable/stock/{symbol}/quote?token={API_TOKEN}' # Construct the URL for the API request by formatting the symbol and API token
        response = requests.get(url) # Send an HTTP GET request to the API endpoint
        data = response.json() # Parse the JSON content of the response into a Python dictionary
        stock_prices[symbol] = data['latestPrice'] # Retrieve the 'latestPrice' field from the parsed JSON data and store it in the dictionary
    return stock_prices # Return the dictionary containing stock prices for each symbol

# Get stock prices for specificed symbols
stock_prices = get_stock_prices(stock_symbols)

# Print stock prices
for symbol, price in stock_prices.items():
    print(f'Current price of {symbol}: ${price}')

# This line defines a function named get_historical_data that takes two parameters: symbol and range
def get_historical_data(symbol, range='1m'): #The range parameter specifies the time range for the historical data. It has a default value of '1m', which represents the past month.
    url = f'https://cloud.iexapis.com/stable/stock/{symbol}/chart/{range}?token={API_TOKEN}'
    response = requests.get(url)
    data = response.json()
    return data

def calculate_7_day_average(data, symbol):  # Add 'symbol' parameter here
    closing_prices = [entry['close'] for entry in data[-7:]]
    average = sum(closing_prices) / 7
    print(f'Current 7-day average for {symbol}: ${average:.2f}')  # Include 'symbol' in the print statement
    return average


# Get 7-day moving averages
seven_day_averages = {}
for symbol in stock_symbols:
    historical_data = get_historical_data(symbol)
    seven_day_average = calculate_7_day_average(historical_data, symbol)  # Pass 'symbol' here
    seven_day_averages[symbol] = seven_day_average
previous_prices = {}

# Inside your check_price_alerts function
def check_price_alerts(current_prices, seven_day_averages, threshold=0.25):
    alerts = []
    for symbol in current_prices:
        if symbol in seven_day_averages:
            price_diff = seven_day_averages[symbol] - current_prices[symbol]
            if price_diff >= threshold:
                print(f"Alert triggered for {symbol}: Current price is below 7-day average by {price_diff:.2f}")
                alerts.append(symbol)
    return alerts

# Get current stock prices
current_prices = get_stock_prices(stock_symbols)

# Check price alerts
alerts = check_price_alerts(current_prices, seven_day_averages)

# Print alerts
if alerts:
    print(f"Price alerts triggered for: {', '.join(alerts)}")
    send_notification_to_ifttt(alerts)
else:
    print("No price alerts triggered.")



# Check price alerts
alerts = check_price_alerts(current_prices, seven_day_averages)

# Call the function to send notifications
send_notification_to_ifttt(alerts)

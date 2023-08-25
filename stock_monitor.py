import requests
import schedule
import time
import os
# IEX Cloud and IFTTT API token
API_TOKEN = os.environ.get('IEX_API_KEY')
IFTTT_KEY = os.environ.get('IFTTT_API_KEY')

# List of stock symbols to monitor
stock_symbols = ['TSLA', 'AAPL', 'MSFT', 'GOOGL', 'NKE']
previous_prices = {symbol: {'price': None, 'timestamp': None} for symbol in stock_symbols}

"""
This function will send alerts to the IFTTT app which will show up as a notification on your
mobile device
"""
def send_notification_to_ifttt(stock_alerts):
    for symbol in stock_alerts:
        url = f'https://maker.ifttt.com/trigger/stock_price_alert/with/key/{IFTTT_KEY}'
        data = {'value1': f'Alert: Price drop for {symbol}'}
        response = requests.post(url, json=data)
        if response.status_code == 200:
            print(f"Notification sent for {symbol}")
        else:
            print(f"Failed to send notification for {symbol}")

"""
Using the IEX API, this function will make a get request for each symbol in the list 'symbols'
which will be defined in the following line (stock_prices)
"""
def get_stock_prices(symbols):
    stock_prices = {}
    for symbol in symbols:
        url = f'https://cloud.iexapis.com/stable/stock/{symbol}/quote?token={API_TOKEN}' # Construct the URL for the API request by formatting the symbol and API token
        response = requests.get(url) # Send an HTTP GET request to the API endpoint
        data = response.json()
        stock_prices[symbol] = data['latestPrice'] # Retrieve the 'latestPrice' field from the parsed JSON data and store it in the dictionary
    return stock_prices # Return the dictionary containing stock prices for each symbol

# Get stock prices for specificed symbols
stock_prices = get_stock_prices(stock_symbols)
# Get previous price for specificed symbols - this will be used
previous_prices = {symbol: {'price': None, 'timestamp': None} for symbol in stock_symbols}

# Quick View of current prices for all stocks
for symbol, price in stock_prices.items():
    print(f'Current price of {symbol}: ${price}')

"""
This line defines a API request named get_historical_data that takes two parameters: symbol and range for the last 7 days.
"""
def get_historical_data(symbol, range='1m'):
    url = f'https://cloud.iexapis.com/stable/stock/{symbol}/chart/{range}?token={API_TOKEN}'
    response = requests.get(url)
    data = response.json()
    return data

"""
This function calculates the 7 day average using the data from the API get request above.
"""
def calculate_7_day_average(closing_prices):
    return sum(closing_prices) / 7
seven_day_averages = {
    symbol: calculate_7_day_average([entry['close'] for entry in get_historical_data(symbol)[-7:]])
    for symbol in stock_symbols
}

"""
This function defines the rule for the alerts. A alert will be triggered if the current price is
at least 0.25 below the 7 day average.
"""
def check_price_alerts(current_prices, seven_day_averages, threshold=0.25):
    alerts = []
    for symbol in current_prices:
        if symbol in seven_day_averages:
            price_diff = seven_day_averages[symbol] - current_prices[symbol]

            # Check if the current price is less than the previous price
            previous_price = previous_prices[symbol]['price']
            if previous_price is not None:
                diff = previous_price - current_prices[symbol]  # Calculate the difference
                if abs(diff) >= threshold:  # Check if the absolute difference is greater than or equal to the threshold
                    print(f"Alert triggered for {symbol}: Price has dropped by more than £0.25!")
                    alerts.append(symbol)
                    send_notification_to_ifttt(alerts)

            # Check if the price drop is above the threshold
            if price_diff >= threshold:
                print(f"Alert triggered for {symbol}: Current price is below 7-day average by {price_diff:.2f}")
                alerts.append(symbol)
                send_notification_to_ifttt(alerts)


    return alerts

"""
This set's a schedule for the script to run every 5 seconds. It also updated the previous price
with the current price and timestamps
"""
current_prices = get_stock_prices(stock_symbols) # Get current stock prices
alerts = check_price_alerts(current_prices, seven_day_averages) #Check price alerts
def run_stock_monitor():
    current_prices = get_stock_prices(stock_symbols)
    seven_day_averages = {
        symbol: calculate_7_day_average([entry['close'] for entry in get_historical_data(symbol)[-7:]])
        for symbol in stock_symbols
    }
    alerts = check_price_alerts(current_prices, seven_day_averages)

    if alerts:
        send_notification_to_ifttt(alerts)
    else:
        print("No price alerts triggered.")
    # Update the previous prices dictionary with the current prices and timestamps
    for symbol in stock_symbols:
        previous_prices[symbol]['price'] = current_prices[symbol]
        previous_prices[symbol]['timestamp'] = time.time()

# Schedule the `run_stock_monitor` function to run every 5 seconds
schedule.every(5).seconds.do(run_stock_monitor)

# Run the scheduled tasks
while True:
    schedule.run_pending()
    time.sleep(1)

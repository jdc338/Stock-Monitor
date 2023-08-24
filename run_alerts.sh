node fetch_stock_data.js

python /Users/jdc338/code/jdc338/xander/StockMonitor/Stock-Monitor/stock_monitor.py


import schedule
import time

def monitor_stock():
    # Your stock monitoring script logic here
    print("Monitoring stocks...")

# Schedule the `monitor_stock` function to run every 15 minutes
schedule.every(15).minutes.do(monitor_stock)

# Run the scheduled tasks
while True:
    schedule.run_pending()
    time.sleep(1)

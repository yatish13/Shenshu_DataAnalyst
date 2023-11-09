import yfinance as yf
from apscheduler.schedulers.background import BackgroundScheduler
from pymongo import MongoClient
from datetime import datetime, timedelta
import pytz

client = MongoClient('mongodb://localhost:27017/')
db = client['stock_data']
collection = db['icici_bank']

def get_store_stock_data():
    now = datetime.now(pytz.timezone("Asia/Kolkata"))
    days_to_subtract = now.weekday()

    start_of_week = now - timedelta(days=days_to_subtract)
    end_of_week = start_of_week + timedelta(days=6)
    formatted_start_date = start_of_week.strftime("%Y-%m-%d")
    formatted_end_date = end_of_week.strftime("%Y-%m-%d")
    start_time = now.replace(hour=11, minute=15, second=0, microsecond=0)
    end_time = now.replace(hour=14, minute=15, second=0, microsecond=0)

    if start_time <= now <= end_time:
        icici = yf.Ticker("ICICIBANK.NS")
        data = icici.history(start=formatted_start_date,end=formatted_end_date,interval='15m')
        data['Datetime'] = data.index
        data.reset_index(drop=True, inplace=True)
        data_dict = data.to_dict(orient='records')
        collection.insert_many(data_dict)
        print(f"Data stored for {now}")
    else:
        
        print(f"Outside of data logging hours at {now}")

# Initialize scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(get_store_stock_data, 'interval', minutes=15)

# Start the scheduler
scheduler.start()

try:
    # Keep the program running
    while True:
        pass
except (KeyboardInterrupt, SystemExit):
    # Shut down the scheduler gracefully
    scheduler.shutdown()
    client.close()
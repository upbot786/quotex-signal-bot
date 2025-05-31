import os
import time
import requests
from datetime import datetime
import pytz

# Load environment variables
BOT_API_TOKEN = os.getenv("BOT_API_TOKEN")
USER_ID = os.getenv("USER_ID")
API_KEY = os.getenv("API_KEY")

# Validate API credentials
if not BOT_API_TOKEN or not USER_ID or not API_KEY:
    raise ValueError("BOT_API_TOKEN, USER_ID, or API_KEY not set.")

# Correct symbol list as per Twelve Data documentation
symbols = [
    "USD/JPY",
    "GBP/USD",
    "ETH/USD",
    "EUR/USD",
    "BTC/USD"
]

# France timezone
tz = pytz.timezone('Europe/Paris')

# Function to fetch data for each symbol
def fetch_price(symbol):
    url = f"https://api.twelvedata.com/time_series?symbol={symbol}&interval=1min&outputsize=1&apikey={API_KEY}"
    response = requests.get(url)
    return response.json()

# Main loop
for symbol in symbols:
    now = datetime.now(tz).strftime("%H:%M:%S")
    print(f"⏰ Checking {symbol} at {now} France time...")

    try:
        data = fetch_price(symbol)

        if 'status' in data and data['status'] == 'error':
            print(f"⚠️ API error for {symbol}: {data}")
        else:
            # Example: print last closing price
            last_price = data['values'][0]['close']
            print(f"✅ Last price for {symbol}: {last_price}")

    except Exception as e:
        print(f"❌ Error while fetching {symbol}: {e}")

    # Wait 8 seconds to stay under free-tier rate limit
    time.sleep(8)

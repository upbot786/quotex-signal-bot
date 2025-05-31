import os
import time
import requests
from datetime import datetime
import pytz

# Load environment variables
BOT_API_TOKEN = os.getenv("BOT_API_TOKEN")
USER_ID = os.getenv("USER_ID")
API_KEY = os.getenv("API_KEY")

# Validate environment variables
if not BOT_API_TOKEN or not USER_ID or not API_KEY:
    raise ValueError("BOT_API_TOKEN, USER_ID, or API_KEY not set.")

# Correct symbol list per Twelve Data format
symbols = [
    "USD/JPY",
    "GBP/USD",
    "ETH/USD",
    "EUR/USD",
    "BTC/USD"
]

# Timezone for France
tz = pytz.timezone('Europe/Paris')

# Send message to Telegram
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_API_TOKEN}/sendMessage"
    payload = {
        "chat_id": USER_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    try:
        response = requests.post(url, data=payload)
        if response.status_code != 200:
            print(f"❌ Telegram error: {response.text}")
    except Exception as e:
        print(f"❌ Telegram send failed: {e}")

# Fetch price from Twelve Data API
def fetch_price(symbol):
    url = f"https://api.twelvedata.com/time_series?symbol={symbol}&interval=1min&outputsize=1&apikey={API_KEY}"
    response = requests.get(url)
    return response.json()

# Main loop (one-time check per symbol)
for symbol in symbols:
    now = datetime.now(tz).strftime("%H:%M:%S")
    print(f"⏰ Checking {symbol} at {now} France time...")

    try:
        data = fetch_price(symbol)

        if 'status' in data and data['status'] == 'error':
            error_msg = f"⚠️ Error for {symbol}: {data['message']}"
            print(error_msg)
            send_telegram_message(error_msg)

        else:
            price = data['values'][0]['close']
            success_msg = f"✅ <b>{symbol}</b>\nCurrent Price: <code>{price}</code>\n🕒 Time: {now} 🇫🇷"
            print(success_msg)
            send_telegram_message(success_msg)

    except Exception as e:
        error_msg = f"❌ Failed to fetch {symbol}: {e}"
        print(error_msg)
        send_telegram_message(error_msg)

    # Sleep 8–10 seconds to avoid API rate limit
    time.sleep(10)

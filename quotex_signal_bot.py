import os
import requests
from datetime import datetime
import time

BOT_API_TOKEN = os.getenv("BOT_API_TOKEN")
USER_ID = os.getenv("USER_ID")
API_KEY = os.getenv("API_KEY")

if not BOT_API_TOKEN or not USER_ID or not API_KEY:
    raise ValueError("Missing environment variables!")

# Correct symbol list (Twelve Data)
symbols = [
    "EUR/USD",
    "USD/JPY",
    "GBP/USD",
    "BTC/USD",
    "ETH/USD"
]

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_API_TOKEN}/sendMessage"
    payload = {
        "chat_id": USER_ID,
        "text": message
    }
    try:
        response = requests.post(url, data=payload)
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Telegram error: {e}")
        return False

def fetch_price(symbol):
    url = f"https://api.twelvedata.com/price?symbol={symbol}&apikey={API_KEY}"
    try:
        response = requests.get(url)
        data = response.json()
        if "price" in data:
            return float(data["price"])
        else:
            return data  # Error dict
    except Exception as e:
        return {"error": str(e)}

def main():
    while True:
        france_time = datetime.utcnow().timestamp() + (2 * 3600)
        now = datetime.fromtimestamp(france_time).strftime("%H:%M:%S")
        print(f"⏰ Checking market at {now} France time...")

        for symbol in symbols:
            result = fetch_price(symbol)
            if isinstance(result, float):
                msg = f"✅ {symbol} price: {result}"
                print(msg)
                send_telegram_message(msg)
            else:
                print(f"⚠️ API error for {symbol}: {result}")

        time.sleep(60)

if __name__ == "__main__":
    main()

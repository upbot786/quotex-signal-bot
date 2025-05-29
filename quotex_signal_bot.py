import os
import requests
from datetime import datetime
import pytz

# Load environment variables
BOT_API_TOKEN = os.getenv("7636996493:AAEa9ddt4okvNj2RyeWGPemvN3NDsQ_wXCc")
USER_ID = os.getenv("7989610604")
API_KEY = os.getenv("2bbdaeca1e7e4010a0833015a50350e8")

# Constants
symbol = "BTC/USD:Binance"
interval = "1min"
timezone = "Europe/Paris"

def fetch_market_data():
    url = f"https://api.twelvedata.com/time_series?symbol={symbol}&interval={interval}&apikey={API_KEY}&outputsize=2"
    response = requests.get(url)
    try:
        data = response.json()
        if "values" in data:
            return data["values"]
        else:
            print(f"⚠️ API returned no values for {symbol}")
            print(f"🧪 Full response: {data}")  # Debug print
            return None
    except Exception as e:
        print(f"❌ Error parsing API response: {e}")
        return None

def calculate_signal(candles):
    if len(candles) < 2:
        return None, 0

    latest = float(candles[0]["close"])
    previous = float(candles[1]["close"])
    
    if latest > previous:
        return "CALL", 7  # Simplified scoring logic
    elif latest < previous:
        return "PUT", 7
    else:
        return None, 0

def send_signal_to_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_API_TOKEN}/sendMessage"
    payload = {
        "chat_id": USER_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print("✅ Signal sent to Telegram.")
    else:
        print(f"❌ Failed to send message: {response.status_code} {response.text}")

def main():
    paris_time = datetime.now(pytz.timezone(timezone)).strftime("%H:%M:%S")
    print(f"⏰ Checking {symbol} at {paris_time} France time...")

    candles = fetch_market_data()
    if not candles:
        print("⚠️ No valid signal to send.")
        return

    signal, score = calculate_signal(candles)
    print(f"📈 Signal: {signal} | Score: {score}/10")

    if signal:
        message = f"📊 *{symbol}*\nSignal: *{signal}*\nScore: *{score}/10*\nTime: *{paris_time}*"
        send_signal_to_telegram(message)
    else:
        print(f"⚠️ No valid signal for {symbol} (Score: {score}/10)")

if __name__ == "__main__":
    main()

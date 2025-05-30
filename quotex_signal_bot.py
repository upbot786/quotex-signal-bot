import os
import requests
import time
from datetime import datetime
import pytz
import telegram

# ✅ Load keys from GitHub Actions secrets
BOT_API_TOKEN = os.getenv("7636996493:AAEa9ddt4okvNj2RyeWGPemvN3NDsQ_wXCc")
USER_ID = os.getenv("7989610604")
API_KEY = os.getenv("2bbdaeca1e7e4010a0833015a50350e8")

# ✅ Initialize Telegram bot
bot = telegram.Bot(token=BOT_API_TOKEN)

# Settings
PAIR = "BTC/USD"
INTERVAL = "1min"
SOURCE = "Binance"  # Optional: TwelveData supports "Binance" source

# France timezone
france_tz = pytz.timezone("Europe/Paris")

def get_market_data():
    url = f"https://api.twelvedata.com/time_series?symbol={PAIR}:{SOURCE}&interval={INTERVAL}&apikey={API_KEY}"
    try:
        response = requests.get(url)
        data = response.json()
        if "status" in data and data["status"] == "error":
            print(f"🧪 Full response: {data}")
            return None
        return data["values"]
    except Exception as e:
        print(f"❌ Error fetching data: {e}")
        return None

def analyze_signal(prices):
    # Very simple signal logic for example
    if not prices or len(prices) < 2:
        return None, 0

    close_now = float(prices[0]["close"])
    close_prev = float(prices[1]["close"])
    score = 0

    if close_now > close_prev:
        signal = "CALL 🔼"
        score = 10
    elif close_now < close_prev:
        signal = "PUT 🔽"
        score = 10
    else:
        signal = "None"
        score = 0

    return signal, score

def send_signal_to_telegram(signal, score):
    if signal == "None":
        print("⚠️ No valid signal to send.")
        return

    now = datetime.now(france_tz).strftime("%H:%M:%S")
    message = f"📊 Signal for {PAIR} at {now} France time:\n\n🔍 Signal: {signal}\n🔥 Power Score: {score}/10"
    bot.send_message(chat_id=USER_ID, text=message)
    print(f"✅ Sent signal to Telegram: {signal}")

def main():
    now = datetime.now(france_tz).strftime("%H:%M:%S")
    print(f"⏰ Checking {PAIR}:{SOURCE} at {now} France time...")

    prices = get_market_data()
    if not prices:
        print(f"⚠️ API returned no values for {PAIR}:{SOURCE}")
        return

    signal, score = analyze_signal(prices)
    print(f"📈 Signal: {signal} | Score: {score}/10")
    send_signal_to_telegram(signal, score)

if __name__ == "__main__":
    main()

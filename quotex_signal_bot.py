import requests
from datetime import datetime
import time
import pytz
import telegram

# 🛠 Replace these with your real keys
BOT_API_TOKEN = "7636996493:AAEa9ddt4okvNj2RyeWGPemvN3NDsQ_wXCc"
USER_ID = "7989610604"
API_KEY = "2bbdaeca1e7e4010a0833015a50350e8"

bot = telegram.Bot(token=BOT_API_TOKEN)

def get_price_data(symbol="BTC/USD:Binance"):
    url = f"https://api.twelvedata.com/time_series?symbol={symbol}&interval=1min&outputsize=2&apikey={API_KEY}"
    response = requests.get(url)
    try:
        data = response.json()
        if "values" in data:
            return data["values"]
        else:
            print("🧪 Full response:", data)
            return None
    except Exception as e:
        print("⚠️ JSON decode error:", e)
        return None

def analyze_data(values):
    if len(values) < 2:
        return None, 0
    last = float(values[0]["close"])
    prev = float(values[1]["close"])
    score = 0
    signal = None

    if last > prev:
        signal = "CALL"
        score = 9
    elif last < prev:
        signal = "PUT"
        score = 9

    return signal, score

def main():
    france_time = datetime.now(pytz.timezone("Europe/Paris")).strftime("%H:%M:%S")
    print(f"⏰ Checking BTC/USD:Binance at {france_time} France time...")
    values = get_price_data("BTC/USD:Binance")
    if not values:
        print("⚠️ API returned no values for BTC/USD:Binance")
        return

    signal, score = analyze_data(values)
    if signal and score >= 9:
        message = f"✅ SIGNAL: {signal}\nScore: {score}/10\nTime: {france_time}"
        print(message)
        bot.send_message(chat_id=USER_ID, text=message)
    else:
        print(f"⚠️ No valid signal to send.")

if __name__ == "__main__":
    main()

import requests
import telegram
import datetime
import time

# ✅ You can use environment variables if deploying securely
# import os
# BOT_API_TOKEN = os.getenv("BOT_API_TOKEN")
# USER_ID = os.getenv("USER_ID")
# API_KEY = os.getenv("API_KEY")

# ✅ Or directly set your values (ONLY IF private)
BOT_API_TOKEN = "7636996493:AAEa9ddt4okvNj2RyeWGPemvN3NDsQ_wXCc"
USER_ID = "7989610604"
API_KEY = "2bbdaeca1e7e4010a0833015a50350e8"

# Initialize the bot
bot = telegram.Bot(token=BOT_API_TOKEN)

def fetch_price(symbol="BTC/USD:Binance"):
    url = f"https://api.twelvedata.com/time_series?symbol={symbol}&interval=1min&apikey={API_KEY}&outputsize=2"
    response = requests.get(url)
    data = response.json()

    if "values" not in data:
        print(f"⚠️ API returned no values for {symbol}")
        print(f"🧪 Full response: {data}")
        return None

    try:
        values = data["values"]
        latest = float(values[0]["close"])
        previous = float(values[1]["close"])
        return latest, previous
    except (KeyError, IndexError, ValueError):
        print("⚠️ Failed to parse prices.")
        return None

def analyze_and_send():
    now = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"⏰ Checking BTC/USD:Binance at {now} France time...")

    prices = fetch_price()
    if not prices:
        print("⚠️ No valid signal to send.")
        return

    latest, previous = prices
    score = 0

    if latest > previous:
        score = 10
        signal = "CALL 📈"
    elif latest < previous:
        score = 10
        signal = "PUT 📉"
    else:
        signal = "None"

    print(f"📊 Signal: {signal} | Score: {score}/10")

    if score >= 9:
        message = f"📊 *Signal Alert!*\n\n🪙 *Pair:* BTC/USD\n🕐 *Time:* {now}\n📈 *Signal:* {signal}\n💯 *Score:* {score}/10"
        bot.send_message(chat_id=USER_ID, text=message, parse_mode=telegram.ParseMode.MARKDOWN)

if __name__ == "__main__":
    analyze_and_send()

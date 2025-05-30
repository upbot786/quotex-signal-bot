import requests
import telegram
from datetime import datetime
from pytz import timezone
import os

# Read from environment (GitHub secrets)
BOT_API_TOKEN = os.getenv("7636996493:AAEa9ddt4okvNj2RyeWGPemvN3NDsQ_wXCc")
USER_ID = os.getenv("7989610604")
API_KEY = os.getenv("2bbdaeca1e7e4010a0833015a50350e8")

# Setup bot
bot = telegram.Bot(token=BOT_API_TOKEN)

# France time
def get_france_time():
    paris = timezone('Europe/Paris')
    return datetime.now(paris).strftime("%H:%M:%S")

# List of symbols (you can add OTC if supported by the API)
symbols = ["BTC/USD", "ETH/USD", "EUR/USD", "USD/JPY", "GBP/USD"]

# Fetch price from TwelveData API
def fetch_price(symbol):
    url = f"https://api.twelvedata.com/price?symbol={symbol}&apikey={API_KEY}"
    response = requests.get(url)
    try:
        data = response.json()
        if "price" in data:
            return float(data["price"])
        else:
            print(f"⚠️ API error for {symbol}: {data}")
            return None
    except Exception as e:
        print(f"❌ Failed to fetch data for {symbol}: {e}")
        return None

# Signal logic: example condition
def generate_signal(symbol, price):
    if price is None:
        return None, 0
    # Simple example signal condition
    if symbol == "BTC/USD" and price > 68000:
        return "CALL", 9
    elif symbol == "BTC/USD" and price < 65000:
        return "PUT", 9
    elif symbol != "BTC/USD" and int(price) % 2 == 0:
        return "CALL", 8
    else:
        return None, 0

# Send signal
def send_signal(symbol, signal, price, score):
    france_time = get_france_time()
    message = (
        f"📊 Signal for {symbol}\n"
        f"⏰ France time: {france_time}\n"
        f"💵 Price: {price}\n"
        f"📈 Signal: {signal} | Power Score: {score}/10"
    )
    bot.send_message(chat_id=USER_ID, text=message)

# Run the bot
def run_bot():
    france_time = get_france_time()
    for symbol in symbols:
        print(f"⏰ Checking {symbol} at {france_time} France time...")
        price = fetch_price(symbol)
        signal, score = generate_signal(symbol, price)
        if signal and score >= 8:
            send_signal(symbol, signal, price, score)
        else:
            print(f"⚠️ No valid signal for {symbol} (Score: {score}/10)")

if __name__ == "__main__":
    run_bot()

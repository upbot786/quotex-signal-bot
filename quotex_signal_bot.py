import os
import requests
import telegram
import pytz
from datetime import datetime

BOT_API_TOKEN = os.getenv("BOT_API_TOKEN")
USER_ID = os.getenv("USER_ID")
API_KEY = os.getenv("API_KEY")

if not BOT_API_TOKEN or not USER_ID or not API_KEY:
    raise ValueError("BOT_API_TOKEN, USER_ID, or API_KEY not set.")

bot = telegram.Bot(token=BOT_API_TOKEN)

# Set timezone
paris = pytz.timezone("Europe/Paris")

# Symbols to check
symbols = ["USD/JPY", "GBP/USD", "ETH/USD", "EUR/USD", "BTC/USD"]

for symbol in symbols:
    now = datetime.now(paris)
    print(f"⏰ Checking {symbol} at {now.strftime('%H:%M:%S')} France time...")

    response = requests.get(
        "https://api.twelvedata.com/price",
        params={"symbol": symbol.replace("/", ""), "apikey": API_KEY}
    ).json()

    if "price" in response:
        price = response["price"]
        message = f"🔔 Signal for {symbol}\nCurrent price: {price}\nTime: {now.strftime('%H:%M:%S')} Paris"
        bot.send_message(chat_id=USER_ID, text=message)
    else:
        print(f"⚠️ API error for {symbol}: {response}")

import requests
from telegram import Bot, ParseMode
from datetime import datetime
import time

# ✅ Your API keys (hardcoded for now — secure in environment vars for production)
BOT_API_TOKEN = "7636996493:AAEa9ddt4okvNj2RyeWGPemvN3NDsQ_wXCc"
USER_ID = "7989610604"
API_KEY = "2bbdaeca1e7e4010a0833015a50350e8"

# Initialize Telegram Bot
bot = Bot(token=BOT_API_TOKEN)

# Function to fetch latest data from TwelveData API
def fetch_price(symbol):
    url = f"https://api.twelvedata.com/time_series?symbol={symbol}&interval=1min&outputsize=1&apikey={API_KEY}"
    response = requests.get(url)
    data = response.json()
    
    if "status" in data and data["status"] == "error":
        print(f"❌ API response error for {symbol}: {data}")
        return None
    try:
        price = float(data["values"][0]["close"])
        return price
    except (KeyError, IndexError, ValueError):
        print(f"⚠️ Unexpected data format: {data}")
        return None

# Generate a dummy signal for now
def generate_signal(symbol):
    price = fetch_price(symbol)
    if price is None:
        return None, 0

    # Example dummy signal logic (placeholder)
    if price > 50000:
        return "BUY", 10
    else:
        return "SELL", 7

# Send signal to Telegram
def send_signal(symbol, signal, score):
    now = datetime.now().strftime("%H:%M:%S")
    message = f"📊 Signal for *{symbol}*\n⏰ Time: *{now}* France time\n📈 Signal: *{signal}* | Score: *{score}/10*"
    bot.send_message(chat_id=USER_ID, text=message, parse_mode=ParseMode.MARKDOWN)

# Main function
def main():
    symbol = "BTC/USD"

    print(f"⏰ Checking {symbol} at {datetime.now().strftime('%H:%M:%S')} France time...")

    signal, score = generate_signal(symbol)

    if signal and score >= 7:
        send_signal(symbol, signal, score)
    else:
        print(f"⚠️ No valid signal for {symbol} (Score: {score}/10)")

if __name__ == "__main__":
    main()

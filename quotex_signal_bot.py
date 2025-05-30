import os
import requests
import telegram
from datetime import datetime
import pytz

# Load secrets from environment variables
BOT_API_TOKEN = os.getenv("7636996493:AAEa9ddt4okvNj2RyeWGPemvN3NDsQ_wXCc")
USER_ID = os.getenv("7989610604")
API_KEY = os.getenv("2bbdaeca1e7e4010a0833015a50350e8")

# Check for missing keys
if not BOT_API_TOKEN or not USER_ID or not API_KEY:
    raise ValueError("BOT_API_TOKEN, USER_ID, or API_KEY not set.")

# Initialize Telegram Bot
bot = telegram.Bot(token=BOT_API_TOKEN)

# Define trading pairs to check
PAIRS = ["BTC/USD", "ETH/USD", "EUR/USD", "GBP/USD", "USD/JPY"]

# Set France time zone
tz = pytz.timezone("Europe/Paris")
now = datetime.now(tz)
current_time = now.strftime("%H:%M:%S")

# Function to get signal score (placeholder logic — customize as needed)
def get_power_score(data):
    try:
        close = float(data["values"][0]["close"])
        open_ = float(data["values"][0]["open"])
        if close > open_:
            return 9  # Example signal score
    except:
        pass
    return 0

# Loop over each pair
for symbol in PAIRS:
    symbol_encoded = symbol.replace("/", "")
    print(f"⏰ Checking {symbol} at {current_time} France time...")

    url = f"https://api.twelvedata.com/time_series?symbol={symbol_encoded}&interval=1min&apikey={API_KEY}&outputsize=1"

    response = requests.get(url)
    data = response.json()

    if "status" in data and data["status"] == "error":
        print(f"❌ API error for {symbol}: {data}")
        continue

    if "values" not in data:
        print(f"⚠️ No values returned for {symbol}")
        continue

    power_score = get_power_score(data)

    if power_score >= 9:
        message = f"✅ Signal for {symbol} at {current_time} (France time)\nPower Score: {power_score}/10\nDirection: CALL 📈"
        bot.send_message(chat_id=USER_ID, text=message)
        print("📤 Signal sent via Telegram.")
    else:
        print(f"⚠️ No strong signal for {symbol} (Score: {power_score}/10)")

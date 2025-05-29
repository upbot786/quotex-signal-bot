import requests
import pytz
import os
from datetime import datetime

# ✅ Load secrets from GitHub Actions environment variables
BOT_API_TOKEN = os.getenv("7636996493:AAEa9ddt4okvNj2RyeWGPemvN3NDsQ_wXCc")
USER_ID = os.getenv("7989610604")
API_KEY = os.getenv("2bbdaeca1e7e4010a0833015a50350e8")

# ✅ Symbol and interval
symbol = "BTC/USD"
interval = "1min"

# ✅ Set timezone
timezone = pytz.timezone("UTC")
now = datetime.now(timezone)
timestamp = now.strftime("%H:%M:%S")

# ✅ Fetch market data from Twelve Data API
url = f"https://api.twelvedata.com/time_series?symbol={symbol.replace('/', '')}&interval={interval}&apikey={API_KEY}&outputsize=2"
response = requests.get(url)
data = response.json()

print(f"\n📊 Checking {symbol} at {timestamp}...")

if "values" not in data:
    print(f"❌ API response error for {symbol}: {data}")
    print("❌ No prices fetched.")
    signal = None
    score = 0
else:
    values = data["values"]
    if len(values) < 2:
        print("❌ Not enough data.")
        signal = None
        score = 0
    else:
        close_1 = float(values[0]["close"])
        close_2 = float(values[1]["close"])

        if close_1 > close_2:
            signal = "CALL"
        elif close_1 < close_2:
            signal = "PUT"
        else:
            signal = "None"

        score = 10 if signal in ["CALL", "PUT"] else 0

        print(f"🔍 Signal: {signal} | Score: {score}/10")

# ✅ Send signal via Telegram if valid
if signal in ["CALL", "PUT"]:
    message = f"📣 *{symbol}* Signal\nTime: {timestamp} UTC\nSignal: *{signal}* 🚀\nScore: {score}/10"
    telegram_url = f"https://api.telegram.org/bot{BOT_API_TOKEN}/sendMessage"
    payload = {
        "chat_id": USER_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    tg_response = requests.post(telegram_url, data=payload)
    if tg_response.status_code == 200:
        print("✅ Signal sent successfully via Telegram.")
    else:
        print(f"❌ Failed to send message: {tg_response.text}")
else:
    print(f"⚠️ No valid signal for {symbol} (Score: {score}/10)")

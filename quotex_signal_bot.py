import os
import requests
import pytz
from datetime import datetime

# ✅ Read secrets from environment variables (GitHub Actions)
BOT_API_TOKEN = os.getenv("7636996493:AAEa9ddt4okvNj2RyeWGPemvN3NDsQ_wXCc")
USER_ID = os.getenv("7989610604")
API_KEY = os.getenv("2bbdaeca1e7e4010a0833015a50350e8")

# ✅ Safety check: Make sure all variables are available
if not BOT_API_TOKEN or not USER_ID or not API_KEY:
    raise Exception("❌ One or more environment variables are missing: BOT_API_TOKEN, USER_ID, or API_KEY.")

# ✅ Define trading pair and interval
pair = "BTC/USD:Binance"
interval = "1min"
url = f"https://api.twelvedata.com/time_series?symbol={pair}&interval={interval}&apikey={API_KEY}"

# ✅ Get current France time
paris = pytz.timezone('Europe/Paris')
now = datetime.now(paris)
print(f"⏰ Checking {pair} at {now.strftime('%H:%M:%S')} France time...")

# ✅ Fetch data from Twelve Data API
try:
    response = requests.get(url)
    data = response.json()

    # Check for API errors
    if "status" in data and data["status"] == "error":
        print(f"⚠️ API returned no values for {pair}")
        print(f"🧪 Full response: {data}")
    elif "values" not in data:
        print(f"❌ No 'values' field in response for {pair}. Full response: {data}")
    else:
        latest = data["values"][0]
        close_price = float(latest["close"])

        print(f"✅ Latest close price: {close_price}")

        # ✅ Dummy signal logic
        signal = "CALL" if close_price % 2 == 0 else "PUT"
        power_score = 9  # Dummy static value

        print(f"📈 Signal: {signal} | Score: {power_score}/10")

        # ✅ Send to Telegram
        telegram_url = f"https://api.telegram.org/bot{BOT_API_TOKEN}/sendMessage"
        message = f"📊 *{pair}*\nSignal: *{signal}*\nPower Score: *{power_score}/10*\nTime: {now.strftime('%H:%M:%S')} 🇫🇷"
        payload = {
            "chat_id": USER_ID,
            "text": message,
            "parse_mode": "Markdown"
        }
        telegram_response = requests.post(telegram_url, data=payload)
        if telegram_response.status_code == 200:
            print("✅ Signal sent to Telegram.")
        else:
            print(f"❌ Failed to send signal. Telegram response: {telegram_response.text}")

except Exception as e:
    print(f"❌ Exception occurred: {e}")

import requests
import datetime
import pytz
from statistics import mean

# === CONFIGURATION ===
BOT_API_TOKEN = "7636996493:AAGbJoYg9wpG-VYuJwLG6prZpd2g1O3yVrI"
USER_ID = "7989610604"
API_KEY = "2bbdaeca1e7e4010a0833015a50350e8"

symbols = ["EUR/USD", "USD/JPY", "GBP/USD", "BTC/USD", "ETH/USD"]

def calculate_ema(prices, period):
    k = 2 / (period + 1)
    ema = prices[0]
    for price in prices[1:]:
        ema = price * k + ema * (1 - k)
    return ema

def calculate_rsi(prices, period=14):
    gains, losses = [], []
    for i in range(1, len(prices)):
        diff = prices[i] - prices[i-1]
        gains.append(max(0, diff))
        losses.append(max(0, -diff))
    if len(gains) < period:
        return 50
    avg_gain = mean(gains[-period:])
    avg_loss = mean(losses[-period:])
    if avg_loss == 0:
        return 100
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

def calculate_macd(prices, fast=12, slow=26, signal_period=9):
    if len(prices) < slow + signal_period:
        return 0, 0, 0
    ema_fast = calculate_ema(prices[-fast:], fast)
    ema_slow = calculate_ema(prices[-slow:], slow)
    macd_line = ema_fast - ema_slow
    signal_line = calculate_ema(prices[-signal_period:], signal_period)
    histogram = macd_line - signal_line
    return macd_line, signal_line, histogram

def get_france_time():
    utc_now = datetime.datetime.utcnow()
    france_tz = pytz.timezone('Europe/Paris')
    return utc_now.replace(tzinfo=pytz.utc).astimezone(france_tz)

def fetch_price_data(symbol):
    url = f"https://api.twelvedata.com/time_series?symbol={symbol}&interval=1min&outputsize=50&apikey={API_KEY}"
    try:
        response = requests.get(url)
        data = response.json()
        if "values" not in data:
            return []
        closes = [float(entry["close"]) for entry in reversed(data["values"])]
        return closes
    except:
        return []

def generate_signal(prices):
    if len(prices) < 26:
        return None, 0
    ema5 = calculate_ema(prices[-5:], 5)
    ema10 = calculate_ema(prices[-10:], 10)
    rsi = calculate_rsi(prices)
    macd, signal, histogram = calculate_macd(prices)

    score = 0
    if ema5 > ema10:
        score += 3
    if 50 < rsi < 70:
        score += 2
    if macd > signal and histogram > 0:
        score += 5

    if score >= 9:
        return "CALL", score
    elif ema5 < ema10 and rsi > 30 and macd < signal and histogram < 0:
        return "PUT", score
    return None, score

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_API_TOKEN}/sendMessage"
    payload = {'chat_id': USER_ID, 'text': message}
    try:
        requests.post(url, data=payload)
    except:
        pass

def save_signal_to_file(message):
    with open("signals.txt", "a") as file:
        file.write(message + "\n")

# === MAIN SCRIPT ===
now = get_france_time()
symbol = symbols[now.minute % len(symbols)]
print(f"📊 Checking {symbol} at {now.strftime('%H:%M:%S')}...")
prices = fetch_price_data(symbol)
signal, score = generate_signal(prices)

if signal:
    trade_time = now + datetime.timedelta(minutes=5)
    time_str = trade_time.strftime("%H:%M")
    message = f"{time_str}  {symbol}  {signal} (Score: {score}/10)"
    send_telegram_message(message)
    save_signal_to_file(message)
    print("✅ Signal sent:", message)
else:
    print(f"⚠️ No valid signal for {symbol} (Score: {score}/10)")

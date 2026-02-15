import telebot
import random
from datetime import datetime, timedelta

TOKEN = "8434399652:AAFRWhgu_9kdjzYkAnsghMUz0AgC-v9zgK0"
bot = telebot.TeleBot(TOKEN)

markets = {
    "CryptoIDX": "crypto",
    "AUD/USD": "audusd",
    "XAU/USD": "xauusd",
    "GBP/USD": "gbpusd"
}

active_signals = {}

def generate_signal():
    return random.choice(["BUY", "SELL"])

def get_signal(market_key):
    now = datetime.utcnow() + timedelta(hours=7)
    expired_time = now + timedelta(minutes=5)

    if market_key in active_signals:
        saved = active_signals[market_key]
        if now < saved["expired"]:
            return saved

    direction = generate_signal()
    signal_data = {
        "direction": direction,
        "time": now.strftime("%H:%M"),
        "date": now.strftime("%Y-%m-%d"),
        "expired": expired_time
    }
    active_signals[market_key] = signal_data
    return signal_data

@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    for market_name, market_key in markets.items():
        markup.add(
            telebot.types.InlineKeyboardButton(text=market_name, callback_data=market_key)
        )
    bot.send_message(
        message.chat.id,
        "🔥 YOYO SIGNAL BOT 🔥\n\nPilih Market:",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    signal = get_signal(call.data)

    if signal["direction"] == "BUY":
        header = "🟢📈 BUY NOW 🔼"
    else:
        header = "🟥📉 SELL NOW 🔽"

    market_name = None
    for name, key in markets.items():
        if key == call.data:
            market_name = name
            break

    text = f"""
{header} |⌚ {signal['date']}
━━━━━━━━━━━━━━━━━━
👉 {signal['time']}  S
📊 MARKET: {market_name}
━━━━━━━━━━━━━━━━━━
⚠️ MAXIMAL K2 | KOMPENSASI SEARAH
⚠️ LIHAT JAM DI GMT+7
⚠️ CARA PAKAINYA -1 MENIT SEBELUM SIGNAL
━━━━━━━━━━━━━━━━━━
©️Copyright by @YOYO SIGNAL BOT
🔄 /start untuk Cek Signal Berikutnya
"""
    bot.send_message(call.message.chat.id, text)

print("Bot running...")
bot.infinity_polling()

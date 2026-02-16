import telebot
import random
import time
from datetime import datetime, timedelta

TOKEN = "8434399652:AAFRWhgu_9kdjzYkAnsghMUz0AgC-v9zgK0"
bot = telebot.TeleBot(TOKEN)

markets = ["CryptoIDX", "Samba_X", "Tropic_X", "Street_X"]

active_signals = {}

def generate_signal(existing_signals):
    """Generate signal acak yang tidak sama dengan existing_signals saat ini"""
    choices = ["BUY", "SELL"]
    random.shuffle(choices)
    for signal in choices:
        if signal not in existing_signals:
            return signal
    return random.choice(choices)  # fallback

def get_signal(market_key):
    now_timestamp = int(time.time())
    if market_key in active_signals:
        saved = active_signals[market_key]
        if now_timestamp < saved["expired"]:
            return saved

    # ambil semua signal market lain untuk saat ini
    other_signals = [v["direction"] for k,v in active_signals.items() if k != market_key and int(time.time()) < v["expired"]]
    direction = generate_signal(other_signals)

    now = datetime.utcnow() + timedelta(hours=7)
    expired_timestamp = now_timestamp + 300  # 5 menit

    signal_data = {
        "direction": direction,
        "time": now.strftime("%H:%M"),
        "date": now.strftime("%Y-%m-%d"),
        "expired": expired_timestamp
    }
    active_signals[market_key] = signal_data
    return signal_data

# START COMMAND
@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    for market_name in markets:
        display_name = f"📊 {market_name}"
        markup.add(telebot.types.InlineKeyboardButton(text=display_name, callback_data=market_name))
    bot.send_message(chat_id, "🔥 YOYO SIGNAL BOT 🔥\n\nPilih Market:", reply_markup=markup)

# CALLBACK HANDLER
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    chat_id = call.message.chat.id
    signal = get_signal(call.data)
    header = "🟢📈 BUY NOW 🔼" if signal["direction"] == "BUY" else "🟥📉 SELL NOW 🔽"
    letter = "B" if signal["direction"] == "BUY" else "S"
    text = f"""
{header} {signal['time']} {letter}
━━━━━━━━━━━━━━━━━━
📊 MARKET: {call.data}
━━━━━━━━━━━━━━━━━━
⚠️ MAXIMAL K2 | KOMPENSASI SEARAH
⚠️ LIHAT JAM DI GMT+7
⚠️ CARA PAKAINYA -1 MENIT SEBELUM SIGNAL
━━━━━━━━━━━━━━━━━━
©️Copyright by @YOYO SIGNAL BOT
🔄 /start untuk Cek Signal Berikutnya
"""
    bot.send_message(chat_id, text)

print("Bot running...")
bot.infinity_polling()

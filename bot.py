import telebot
import random
import json
from datetime import datetime, timedelta

TOKEN = "8434399652:AAFRWhgu_9kdjzYkAnsghMUz0AgC-v9zgK0"
bot = telebot.TeleBot(TOKEN)

DATA_FILE = "signals.json"

markets = {
    "crypto": "📊 CryptoIDX",
    "samba": "📊 Samba_X",
    "tropic": "📊 Tropic_X",
    "street": "📊 Street_X"
}

# ================= LOAD & SAVE =================

def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

active_signals = load_data()

# ================= SIGNAL =================

def generate_signal():
    return random.choice(["BUY 🟢", "SELL 🔴"])

def get_signal(market_key):
    if market_key in active_signals:
        return active_signals[market_key]

    now = datetime.utcnow() + timedelta(hours=7)
    entry_time = now + timedelta(minutes=5)

    signal_data = {
        "direction": generate_signal(),
        "time": entry_time.strftime("%H:%M")
    }

    active_signals[market_key] = signal_data
    save_data(active_signals)

    return signal_data

# ================= TELEGRAM =================

@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)

    buttons = [
        telebot.types.InlineKeyboardButton("📊 CryptoIDX", callback_data="crypto"),
        telebot.types.InlineKeyboardButton("📊 Samba_X", callback_data="samba"),
        telebot.types.InlineKeyboardButton("📊 Tropic_X", callback_data="tropic"),
        telebot.types.InlineKeyboardButton("📊 Street_X", callback_data="street"),
    ]

    markup.add(buttons[0], buttons[1])
    markup.add(buttons[2], buttons[3])

    bot.send_message(message.chat.id, "🔥 YOYO SIGNAL BOT 🔥\n\nPilih Market:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    market_key = call.data
    signal = get_signal(market_key)

    text = f"""
{signal['direction']} {signal['time']}
━━━━━━━━━━━━━━━━━━
{markets[market_key]}
━━━━━━━━━━━━━━━━━━
⚠️ MAXIMAL K2 | KOMPENSASI SEARAH
⚠️ LIHAT JAM DI GMT+7
⚠️ CARA PAKAINYA -1 MENIT SEBELUM SIGNAL
━━━━━━━━━━━━━━━━━━
©️ YOYO SIGNAL BOT
"""

    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          text=text)

print("Bot running...")
bot.infinity_polling()

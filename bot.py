import json
import random
from datetime import datetime, timedelta
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

TOKEN = "8434399652:AAFRWhgu_9kdjzYkAnsghMUz0AgC-v9zgK0"
DATA_FILE = "signals.json"

MARKETS = {
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

# ================= SIGNAL LOGIC =================

def generate_signal():
    return random.choice(["BUY 🟢", "SELL 🔴"])

def get_signal(market_key):
    # Kalau sudah pernah ada signal → pakai yang lama
    if market_key in active_signals:
        return active_signals[market_key]

    # Kalau belum ada → generate baru
    now = datetime.utcnow() + timedelta(hours=7)  # WIB
    entry_time = now + timedelta(minutes=5)

    signal_data = {
        "direction": generate_signal(),
        "time": entry_time.strftime("%H:%M")
    }

    active_signals[market_key] = signal_data
    save_data(active_signals)

    return signal_data

# ================= TELEGRAM =================

def start(update: Update, context: CallbackContext):
    keyboard = [
        [
            InlineKeyboardButton("📊 CryptoIDX", callback_data="crypto"),
            InlineKeyboardButton("📊 Samba_X", callback_data="samba")
        ],
        [
            InlineKeyboardButton("📊 Tropic_X", callback_data="tropic"),
            InlineKeyboardButton("📊 Street_X", callback_data="street")
        ]
    ]

    update.message.reply_text(
        "🔥 YOYO SIGNAL BOT 🔥\n\nPilih Market:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

def button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    market_key = query.data
    signal = get_signal(market_key)

    text = f"""
{signal['direction']} {signal['time']}
━━━━━━━━━━━━━━━━━━
{MARKETS[market_key]}
━━━━━━━━━━━━━━━━━━
⚠️ MAXIMAL K2 | KOMPENSASI SEARAH
⚠️ LIHAT JAM DI GMT+7
⚠️ CARA PAKAINYA -1 MENIT SEBELUM SIGNAL
━━━━━━━━━━━━━━━━━━
©️ YOYO SIGNAL BOT
"""

    query.edit_message_text(text=text)

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()

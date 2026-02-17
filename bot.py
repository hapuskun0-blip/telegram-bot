import telebot
import random
from datetime import datetime, timedelta
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# ==============================
# CONFIG
# ==============================

TOKEN = "8434399652:AAFRWhgu_9kdjzYkAnsghMUz0AgC-v9zgK0"
bot = telebot.TeleBotTOKEN)

# ==============================
# FUNCTION GENERATE SIGNAL
# ==============================

def generate_signal():
    return random.choice(["BUY 📈", "SELL 📉"])

def get_signal():
    # WIB = UTC + 7
    now = datetime.utcnow() + timedelta(hours=7)

    # Entry +5 menit dari waktu klik
    entry_time = now + timedelta(minutes=5)

    signal_data = {
        "direction": generate_signal(),
        "time": entry_time.strftime("%H:%M")
    }

    return signal_data

# ==============================
# COMMAND START
# ==============================

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "🔥 YOYO SIGNAL BOT 🔥\n\nKlik /signal untuk ambil signal."
    )

# ==============================
# COMMAND SIGNAL
# ==============================

@bot.message_handler(commands=['signal'])
def signal_menu(message):
    markup = InlineKeyboardMarkup()

    markup.add(
        InlineKeyboardButton("EUR/USD", callback_data="eurusd"),
        InlineKeyboardButton("GBP/USD", callback_data="gbpusd")
    )
    markup.add(
        InlineKeyboardButton("USD/JPY", callback_data="usdjpy"),
        InlineKeyboardButton("Gold (XAUUSD)", callback_data="xauusd")
    )

    bot.send_message(
        message.chat.id,
        "📊 Pilih Market:",
        reply_markup=markup
    )

# ==============================
# CALLBACK MARKET
# ==============================

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):

    market_name = call.data.upper()

    signal = get_signal()

    text = f"""
🔥 YOYO SIGNAL 🔥

Market : {market_name}
Signal : {signal['direction']}
Entry  : {signal['time']} WIB
TF     : M5

Good Luck Bro 🚀
"""

    bot.send_message(call.message.chat.id, text)
    bot.answer_callback_query(call.id)

# ==============================
# RUN BOT
# ==============================

print("Bot is running...")
bot.infinity_polling()

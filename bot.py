import telebot
import random
from datetime import datetime, timedelta

TOKEN = "8434399652:AAFRWhgu_9kdjzYkAnsghMUz0AgC-v9zgK0"
bot = telebot.TeleBot(TOKEN)

markets = {
    "crypto": "📊 CryptoIDX",
    "samba": "📊 Samba_X",
    "tropic": "📊 Tropic_X",
    "street": "📊 Street_X"
}

# ================= SIGNAL =================

def generate_signal():
    return random.choice(["BUY 🟢", "SELL 🔴"])

def get_signal():
    # WIB (GMT+7)
    now = datetime.utcnow() + timedelta(hours=7)
    entry_time = now + timedelta(minutes=5)

    return {
        "direction": generate_signal(),
        "time": entry_time.strftime("%H:%M")
    }

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
    signal = get_signal()
    market_name = markets.get(call.data, "Unknown Market")

    text = f"""
{signal['direction']} {signal['time']}
━━━━━━━━━━━━━━━━━━
{market_name}
━━━━━━━━━━━━━━━━━━
⚠️ MAXIMAL K2 | KOMPENSASI SEARAH
⚠️ LIHAT JAM DI GMT+7
⚠️ CARA PAKAINYA -1 MENIT SEBELUM SIGNAL
━━━━━━━━━━━━━━━━━━
©️ YOYO SIGNAL BOT
"""

    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=text
    )

print("Bot running...")
bot.infinity_polling()

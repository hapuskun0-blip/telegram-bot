import telebot
import random
import time
from datetime import datetime, timedelta

TOKEN = "8434399652:AAFRWhgu_9kdjzYkAnsghMUz0AgC-v9zgK0"
bot = telebot.TeleBot(TOKEN)

markets = {
    "crypto": "📊 CryptoIDX",
    "samba": "📊 Samba_X",
    "tropic": "📊 Tropic_X",
    "street": "📊 Street_X"
}

active_signals = {}

# ================= SIGNAL =================

def generate_signal():
    return random.choice(["BUY 🟢", "SELL 🔴"])


def get_signal(market_key):
    now = datetime.utcnow() + timedelta(hours=7)

    if market_key in active_signals:
        saved = active_signals[market_key]

        entry_time = datetime.strptime(saved["time"], "%H:%M")
        entry_time = entry_time.replace(
            year=now.year,
            month=now.month,
            day=now.day
        )

        # tahan sampai detik 59
        entry_time = entry_time + timedelta(seconds=59)

        if now <= entry_time:
            return saved

    # bikin signal baru
    new_entry = now + timedelta(minutes=5)

    new_signal = {
        "direction": generate_signal(),
        "time": new_entry.strftime("%H:%M")
    }

    active_signals[market_key] = new_signal
    return new_signal


# ================= TELEGRAM =================

@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)

    btn1 = telebot.types.InlineKeyboardButton("📊 CryptoIDX", callback_data="crypto")
    btn2 = telebot.types.InlineKeyboardButton("📊 Samba_X", callback_data="samba")
    btn3 = telebot.types.InlineKeyboardButton("📊 Tropic_X", callback_data="tropic")
    btn4 = telebot.types.InlineKeyboardButton("📊 Street_X", callback_data="street")

    markup.add(btn1, btn2)
    markup.add(btn3, btn4)

    bot.send_message(
        message.chat.id,
        "🔥 YOYO SIGNAL BOT 🔥\n\nPilih Market:",
        reply_markup=markup
    )


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    try:
        # Popup kecil loading
        bot.answer_callback_query(call.id, "⏳ Generating signal...")

        time.sleep(2)  # Delay 2 detik

        signal = get_signal(call.data)
        market_name = markets.get(call.data, "Unknown Market")

        text = (
            f"{signal['direction']} {signal['time']}\n"
            "━━━━━━━━━━━━━━━━━━\n"
            f"{market_name}\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "⚠️ MAXIMAL K2 | KOMPENSASI SEARAH\n"
            "⚠️ LIHAT JAM DI GMT+7\n"
            "⚠️ CARA PAKAINYA -1 MENIT SEBELUM SIGNAL\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "©️ YOYO SIGNAL BOT"
        )

        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=text
        )

    except Exception as e:
        print("ERROR:", e)


print("Bot running...")
bot.infinity_polling()

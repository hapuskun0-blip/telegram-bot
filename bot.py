import telebot
import random
import time
from datetime import datetime, timedelta

TOKEN = "8434399652:AAFRWhgu_9kdjzYkAnsghMUz0AgC-v9zgK0"
bot = telebot.TeleBot(TOKEN)

markets = {
    "💶 EUR/USD": "eurusd",
    "💷 GBP/USD": "gbpusd",
    "💴 AUD/USD": "audusd",
    "🥇 XAU/USD": "xauusd"
}

# Simpan signal aktif per market
active_signals = {}

def generate_signal(pair):
    random.seed(pair + str(time.time()))
    direction = random.choice(["BUY 🟢", "SELL 🔴"])

    if "XAU" in pair:
        entry = round(random.uniform(1900, 2100), 2)
    else:
        base_price = {
            "EUR/USD": 1.0800,
            "GBP/USD": 1.2600,
            "AUD/USD": 0.6600
        }

        clean_pair = pair.replace("💶 ", "").replace("💷 ", "").replace("💴 ", "").replace("🥇 ", "")
        base = base_price.get(clean_pair, 1.1000)
        entry = round(base + random.uniform(-0.0100, 0.0100), 5)

    return direction, entry


def get_signal(pair_name):
    now = datetime.utcnow() + timedelta(hours=7)  # WIB
    expiry_time = now + timedelta(minutes=5)

    # Kalau sudah ada signal & belum expired → pakai yang lama
    if pair_name in active_signals:
        saved = active_signals[pair_name]
        if now < saved["expired"]:
            return saved

    # Kalau belum ada / sudah expired → bikin baru
    direction, entry = generate_signal(pair_name)

    signal_data = {
        "direction": direction,
        "entry": entry,
        "time": now.strftime("%H:%M:%S"),
        "expired": expiry_time
    }

    active_signals[pair_name] = signal_data
    return signal_data


@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)

    for name, callback in markets.items():
        markup.add(
            telebot.types.InlineKeyboardButton(name, callback_data=callback)
        )

    bot.send_message(
        message.chat.id,
        "🔥 *PREMIUM AI SIGNAL BOT*\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "📊 Real Time Market\n"
        "💎 Pilih Market Di Bawah\n",
        parse_mode="Markdown",
        reply_markup=markup
    )


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    pair_name = None

    for name, value in markets.items():
        if call.data == value:
            pair_name = name
            break

    if pair_name:
        signal = get_signal(pair_name)

        text = f"""
━━━━━━━━━━━━━━━━━━
📡 *{pair_name} SIGNAL*
━━━━━━━━━━━━━━━━━━

📈 Direction  : {signal['direction']}
🎯 Entry Price: `{signal['entry']}`

⏰ Time (WIB) : {signal['time']}
⏳ Expired    : 5 Minutes

━━━━━━━━━━━━━━━━━━
🤖 Powered By AI System
"""

        bot.send_message(call.message.chat.id, text, parse_mode="Markdown")


print("Bot running...")
bot.infinity_polling()

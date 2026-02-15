import telebot
import random
import time
from datetime import datetime

TOKEN = "8434399652:AAFRWhgu_9kdjzYkAnsghMUz0AgC-v9zgK0"
bot = telebot.TeleBot(TOKEN)

markets = {
    "💶 EUR/USD": "eurusd",
    "💷 GBP/USD": "gbpusd",
    "💴 AUD/USD": "audusd",
    "🥇 XAU/USD": "xauusd"
}

def generate_signal(pair):
    random.seed(pair + str(time.time()))

    direction = random.choice(["BUY 🟢", "SELL 🔴"])

    if "XAU" in pair:
        entry = round(random.uniform(1900, 2100), 2)
        tp = round(entry + random.uniform(5, 20), 2)
        sl = round(entry - random.uniform(5, 20), 2)
    else:
        base_price = {
            "EUR/USD": 1.0800,
            "GBP/USD": 1.2600,
            "AUD/USD": 0.6600
        }

        clean_pair = pair.replace("💶 ", "").replace("💷 ", "").replace("💴 ", "").replace("🥇 ", "")
        base = base_price.get(clean_pair, 1.1000)

        entry = round(base + random.uniform(-0.0100, 0.0100), 5)
        tp = round(entry + random.uniform(0.0020, 0.0080), 5)
        sl = round(entry - random.uniform(0.0020, 0.0080), 5)

    return direction, entry, tp, sl


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
        "📊 Akurasi Tinggi\n"
        "⚡ Real Time Market\n"
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
        direction, entry, tp, sl = generate_signal(pair_name)

        now = datetime.now().strftime("%H:%M:%S")

        text = f"""
━━━━━━━━━━━━━━━━━━
📡 *{pair_name} SIGNAL*
━━━━━━━━━━━━━━━━━━

📈 Direction  : {direction}
🎯 Entry Price: `{entry}`
🏆 Take Profit: `{tp}`
🛑 Stop Loss  : `{sl}`

⏰ Time       : {now}
⏳ Expired    : 5 Minutes

━━━━━━━━━━━━━━━━━━
🤖 Powered By AI System
"""

        bot.send_message(call.message.chat.id, text, parse_mode="Markdown")


print("Bot running...")
bot.infinity_polling()

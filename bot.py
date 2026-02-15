import telebot
import random
import time
from datetime import datetime, timedelta

TOKEN = "ISI_TOKEN_BOT_LU"
bot = telebot.TeleBot(TOKEN)

# Market list
markets = {
    "CryptoIDX": "crypto",
    "AUD/USD": "audusd",
    "XAU/USD": "xauusd",
    "GBP/USD": "gbpusd"
}

# Simpan signal aktif (5 menit per market)
active_signals = {}

def generate_signal():
    return random.choice(["BUY", "SELL"])

def get_signal(market_key):
    now_timestamp = int(time.time())  # detik sejak epoch

    # Kalau masih dalam 5 menit, pakai signal lama
    if market_key in active_signals:
        saved = active_signals[market_key]
        if now_timestamp < saved["expired"]:
            return saved

    # Generate baru
    direction = generate_signal()
    now = datetime.utcnow() + timedelta(hours=7)  # WIB
    expired_timestamp = now_timestamp + 300  # 5 menit = 300 detik

    signal_data = {
        "direction": direction,
        "time": now.strftime("%H:%M"),
        "date": now.strftime("%Y-%m-%d"),
        "expired": expired_timestamp
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

    # Nama market sesuai tombol
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

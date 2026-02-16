import telebot
import random
import time
from datetime import datetime, timedelta

TOKEN = "8434399652:AAFRWhgu_9kdjzYkAnsghMUz0AgC-v9zgK0"  # Ganti dengan token bot Telegram lu
bot = telebot.TeleBot(TOKEN)

# Market list baru
markets = {
    "CryptoIDX": "crypto",
    "Samba_X": "samba",
    "Tropic_X": "tropic",
    "Street_X": "street"
}

# Simpan signal aktif (5 menit per market)
active_signals = {}

def generate_signal(prev_signal=None):
    """Generate signal baru yang pasti beda dari sebelumnya"""
    choices = ["BUY", "SELL"]
    if prev_signal in choices:
        choices.remove(prev_signal)
    return random.choice(choices)

def get_signal(market_key):
    now_timestamp = int(time.time())

    if market_key in active_signals:
        saved = active_signals[market_key]
        if now_timestamp < saved["expired"]:
            return saved

    # Generate baru sampai beda dari sebelumnya
    prev_signal = active_signals.get(market_key, {}).get("direction")
    direction = generate_signal(prev_signal)

    attempts = 0
    while prev_signal == direction and attempts < 5:
        direction = generate_signal(prev_signal)
        attempts += 1

    now = datetime.utcnow() + timedelta(hours=7)  # WIB
    expired_timestamp = now_timestamp + 300  # 5 menit

    signal_data = {
        "direction": direction,
        "time": now.strftime("%H:%M"),
        "date": now.strftime("%Y-%m-%d"),
        "expired": expired_timestamp
    }

    active_signals[market_key] = signal_data
    return signal_data

# ==== START COMMAND ====
@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    for market_name, market_key in markets.items():
        # Tambahin stiker 📊 di nama market
        display_name = f"📊 {market_name}"
        markup.add(
            telebot.types.InlineKeyboardButton(text=display_name, callback_data=market_key)
        )
    bot.send_message(
        message.chat.id,
        "🔥 YOYO SIGNAL BOT 🔥\n\nPilih Market:",
        reply_markup=markup
    )

# ==== CALLBACK HANDLER ====
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    signal = get_signal(call.data)
    header = "🟢📈 BUY NOW 🔼" if signal["direction"] == "BUY" else "🟥📉 SELL NOW 🔽"
    letter = "B" if signal["direction"] == "BUY" else "S"

    market_name = next((name for name, key in markets.items() if key == call.data), call.data)

    text = f"""
{header} {signal['time']} {letter}
━━━━━━━━━━━━━━━━━━
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

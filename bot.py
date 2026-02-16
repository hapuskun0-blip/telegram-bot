import telebot
import random
import time
from datetime import datetime, timedelta
import threading

TOKEN = "8434399652:AAFRWhgu_9kdjzYkAnsghMUz0AgC-v9zgK0"
bot = telebot.TeleBot(TOKEN)

markets = ["CryptoIDX", "Samba_X", "Tropic_X", "Street_X"]

# Simpan signal aktif per market
active_signals = {}

def generate_signal():
    return random.choice(["BUY", "SELL"])

def get_signal(market_key):
    now = datetime.utcnow() + timedelta(hours=7)  # WIB sekarang
    signal_time = now + timedelta(minutes=5)       # jam +5 menit
    signal_time_str = signal_time.strftime("%H:%M")

    # Simpan signal per market
    direction = generate_signal()
    active_signals[market_key] = {
        "direction": direction,
        "time": signal_time_str,
        "expires": (now + timedelta(minutes=5)).timestamp()
    }
    return active_signals[market_key]

def build_signal_text(market):
    sig = get_signal(market)
    header = "🟢📈 BUY NOW 🔼" if sig["direction"] == "BUY" else "🟥📉 SELL NOW 🔽"
    letter = "B" if sig["direction"] == "BUY" else "S"

    text = f"""
{header} {sig['time']} {letter}
━━━━━━━━━━━━━━━━━━
📊 MARKET: {market}
━━━━━━━━━━━━━━━━━━
⚠️ MAXIMAL K2 | KOMPENSASI SEARAH
⚠️ LIHAT JAM DI GMT+7
⚠️ CARA PAKAINYA -1 MENIT SEBELUM SIGNAL
━━━━━━━━━━━━━━━━━━
©️Copyright by @YOYO SIGNAL BOT
🔄 /start untuk Cek Signal Berikutnya
"""
    return text

# Fungsi update tiap 5 menit
def auto_update(chat_id, msg_id, market):
    while True:
        try:
            new_text = build_signal_text(market)
            bot.edit_message_text(chat_id=chat_id, message_id=msg_id, text=new_text)
        except Exception as e:
            print("Error editing message:", e)
        time.sleep(300)  # 5 menit

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
    market = call.data
    text = build_signal_text(market)
    
    # Kirim signal di pesan baru tapi akan update tiap 5 menit
    msg = bot.send_message(chat_id, text)

    threading.Thread(target=auto_update, args=(chat_id, msg.message_id, market)).start()

print("Bot running...")
bot.infinity_polling()

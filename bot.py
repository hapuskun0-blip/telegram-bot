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

def generate_signal(existing_signals=[]):
    """Signal acak yang tidak sama dengan market lain saat ini"""
    choices = ["BUY", "SELL"]
    random.shuffle(choices)
    for sig in choices:
        if sig not in existing_signals:
            return sig
    return random.choice(choices)

def get_signal(market_key):
    now_timestamp = int(time.time())
    if market_key in active_signals:
        saved = active_signals[market_key]
        if now_timestamp < saved["expired"]:
            return saved

    other_signals = [v["direction"] for k,v in active_signals.items() if k != market_key and int(time.time()) < v["expired"]]
    direction = generate_signal(other_signals)

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
©️Copyright by @yoyotrader01
🔄 /start untuk Cek Signal Berikutnya
"""
    return text

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
    text = build_signal_text(call.data)
    
    # Kirim signal di pesan baru tapi tetap format YOYO
    msg = bot.send_message(chat_id, text)

    # Mulai thread update tiap 5 menit di pesan yang sama
    def auto_update(chat_id, msg_id, market):
        while True:
            try:
                new_text = build_signal_text(market)
                bot.edit_message_text(chat_id=chat_id, message_id=msg_id, text=new_text)
            except Exception as e:
                print("Error editing message:", e)
            time.sleep(300)  # 5 menit

    threading.Thread(target=auto_update, args=(chat_id, msg.message_id, call.data)).start()

print("Bot running...")
bot.infinity_polling()

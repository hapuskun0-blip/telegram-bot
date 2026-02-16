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

# Simpan message_id untuk edit
message_tracker = {}

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

def build_signal_text():
    lines = []
    for market in markets:
        sig = get_signal(market)
        header = "🟢📈 BUY NOW 🔼" if sig["direction"] == "BUY" else "🟥📉 SELL NOW 🔽"
        letter = "B" if sig["direction"] == "BUY" else "S"
        lines.append(f"{header} {sig['time']} {letter} | 📊 {market}")
    return "━━━━━━━━━━━━━━━━━━\n".join(lines)

# Fungsi update message setiap 5 menit
def auto_update(chat_id, msg_id):
    while True:
        try:
            text = build_signal_text()
            bot.edit_message_text(chat_id=chat_id, message_id=msg_id, text=text)
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
    msg = bot.send_message(chat_id, "🔥 YOYO SIGNAL BOT 🔥\n\nPilih Market:", reply_markup=markup)
    
    # Simpan message_id → mulai auto-update
    threading.Thread(target=auto_update, args=(chat_id, msg.message_id)).start()

# CALLBACK HANDLER
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    chat_id = call.message.chat.id
    text = build_signal_text()
    bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=text)

print("Bot running...")
bot.infinity_polling()

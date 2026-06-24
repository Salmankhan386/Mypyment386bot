import os
import time
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# --- CONFIGURATION ---
API_TOKEN = '8843652755:AAEgPsT-ZVQcYnkH9ZmlP2OdVtpW1PViLp4' 
ADMIN_ID = 6724590786  # Muhammad Salman ID
CHANNEL_ID = '-1003856215791' # Spike VIP Signals ID

bot = telebot.TeleBot(API_TOKEN)

# --- HANDLERS ---

@bot.message_handler(commands=['start'])
def send_welcome(message):
    payment_text = (
        "✨ **Spike Vip Manager** ✨\n\n"
        "Welcome! 🚀 To join our VIP signals channel, please pay the subscription fee:\n\n"
        "🔸 **Option 1: EasyPaisa**\n"
        "➔ Account Number: `03169370386`\n"
        "➔ Account Name: *Muhammad Salman*\n"
        "➔ Amount: *1500 PKR*\n\n"
        "🔸 **Option 2: Binance Pay**\n"
        "➔ Pay ID: `385450862`\n"
        "➔ Amount: *$7 USDT*\n\n"
        "🔸 **Option 3: USDT (TRC20)**\n"
        "➔ Address: `TEqfLhNxgmN1ux7LnGuWZq3Hy39K12XQiY`\n\n"
        "⚠️ **Step 2:** After payment, send your transaction screenshot directly to this bot.\n"
        "I will verify and send you the official VIP Access Link immediately!"
    )
    bot.send_message(message.chat.id, payment_text, parse_mode='Markdown')

@bot.message_handler(content_types=['photo'])
def handle_screenshot(message):
    bot.reply_to(message, "Screenshot received! Waiting for Admin approval.")
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("Approve ✅", callback_data=f"approve_{message.chat.id}"),
        InlineKeyboardButton("Reject ❌", callback_data=f"reject_{message.chat.id}")
    )
    username = message.from_user.username if message.from_user.username else "No Username"
    
    try:
        bot.send_message(ADMIN_ID, f"📩 **New Payment Proof!**\nFrom: @{username}")
        bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)
        bot.send_message(ADMIN_ID, "Confirm payment:", reply_markup=markup)
    except Exception as e:
        print(f"❌ Admin Notification Failed: {e}")

@bot.callback_query_handler(func=lambda call: call.data.startswith(('approve_', 'reject_')))
def handle_action(call):
    client_id = call.data.split('_')[1]
    
    if call.data.startswith('approve_'):
        try:
            # NO EXPIRY LIMIT: Kisi qism ki koi member limit ya time limit nahi hai
            invite_link = bot.create_chat_invite_link(
                CHANNEL_ID,
                member_limit=None,
                expire_date=None,
                creates_join_request=False
            ).invite_link
            
            # Message text bilkul badal diya hai taake pata chale naya code chal raha hai
            bot.send_message(client_id, f"🎉 **Congratulations! Your Payment is Approved!**\n\nClick the permanent link below to join the VIP Channel:\n👇👇👇\n{invite_link}\n\n🟢 *Yeh link hamesha active rahega.*")
            bot.answer_callback_query(call.id, "Permanent Link Sent!")
            bot.edit_message_text(f"✅ Approved & Permanent Link Sent to: {client_id}", chat_id=ADMIN_ID, message_id=call.message.message_id)
        except Exception as e:
            bot.send_message(ADMIN_ID, f"❌ Link Generation Error: {e}")

    elif call.data.startswith('reject_'):
        try:
            bot.send_message(client_id, "❌ **Rejected.** Payment not verified.")
            bot.answer_callback_query(call.id, "Rejected!")
            bot.edit_message_text(f"❌ Rejected for {client_id}", chat_id=ADMIN_ID, message_id=call.message.message_id)
        except Exception as e:
            print(f"Reject error: {e}")

# --- RUN ---
if __name__ == "__main__":
    print("Bot is starting...")
    try:
        bot.delete_webhook(drop_pending_updates=True)
    except Exception as e:
        pass
        
    time.sleep(1)
    
    while True:
        try:
            print("Starting polling...")
            bot.polling(none_stop=True)
        except Exception as e:
            time.sleep(5)

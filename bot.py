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
        "I will verify and you will be added directly!"
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
    client_id = int(call.data.split('_')[1])
    
    if call.data.startswith('approve_'):
        try:
            # DIRECT APPROVE: Yeh line user ko bina kisi link ke sidha andar daal degi
            bot.approve_chat_join_request(CHANNEL_ID, client_id)
            
            bot.send_message(client_id, "✅ **Approved!**\n\nAapko VIP Channel mein add kar diya gaya hai. Apna Telegram check karein, channel aapki chat list mein aa chuka hoga! 🎉")
            bot.answer_callback_query(call.id, "User Approved & Added!")
            bot.edit_message_text(f"✅ Approved and Directly Added: {client_id}", chat_id=ADMIN_ID, message_id=call.message.message_id)
        except Exception as e:
            bot.send_message(ADMIN_ID, f"❌ Direct Add Error: {e}\n\n⚠️ *Note:* Ensure karein ke user ne channel par 'Join Request' bheji hui ho.")

    elif call.data.startswith('reject_'):
        try:
            # Decline request if needed
            bot.decline_chat_join_request(CHANNEL_ID, client_id)
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
        print("Webhook cleared.")
    except Exception as e:
        print(f"Webhook error: {e}")
        
    time.sleep(2)
    
    while True:
        try:
            print("Starting polling...")
            bot.polling(none_stop=True)
        except Exception as e:
            print(f"Polling error: {e}")
            time.sleep(5)

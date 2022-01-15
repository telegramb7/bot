import os
from dotenv import load_dotenv
import telebot

load_dotenv()

# initialization bot
token = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(token)

# just an echo bot
@bot.message_handler(content_types="text")
def start_message(message):
    bot.send_message(message.chat.id, message.text)


# polling
bot.polling(none_stop=True, interval=0)

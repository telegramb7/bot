import os
from dotenv import load_dotenv
import telebot
import functions
from telebot import types

load_dotenv()

# initialization bot
token = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(token)

data = {
            'name':'',
            'age':'',
            "description":'',
            "file_unique_id":'',
            "sex":'',

        }

@bot.message_handler(content_types=['text'])
def start_message(message):
    if message.text == '/start':
        id_chat = message.chat.id
        check = functions.check_user_in_db(id_chat)
        if check == False:
            functions.create_new_user(id_chat)
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            hi = types.KeyboardButton('Хауди хо ботяра')
            markup.row(hi)
            bot.send_message(message.from_user.id, text='Привет Новый пользователь. Поздороваешься?:)', reply_markup=markup)
            bot.register_next_step_handler(message, create_anketa)
        elif check == True:
            bot.send_message(message.from_user.id, text=f'Привет {message.chat.first_name}')
    
@bot.message_handler(content_types=['text', 'photo'])
def create_anketa(message):
    if message.text == 'Хауди хо ботяра':
        bot.send_message(message.chat.id, text='Привет. Давай познакомимся, как тебя зовут?')
        bot.register_next_step_handler(message, get_name)
    
def get_name(message):
    global data
    name = message.text
    data['name'] = name
    print(data)
    bot.send_message(message.chat.id, text = 'Введите ваш возраст: ')
    bot.register_next_step_handler(message, get_age)

def get_age(message):
    global data
    age = message.text
    data['age'] = age
    print(data)
    bot.send_message(message.chat.id, text = 'Кратко опишите себя и свои увлечения: ')
    bot.register_next_step_handler(message, get_description)

def get_description(message):
    global data
    description = message.text
    data['description'] = description
    print(data)
    bot.send_message(message.chat.id, text = 'Прикрепите свое фото или короткое фидео: ')
    bot.register_next_step_handler(message, get_file)

def get_file(message):
    global data
    #может упасть если будет текст
    file_unique_id = message.photo[-1].file_id
    data['file_unique_id'] = file_unique_id
    print(data)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    male = types.KeyboardButton('male')
    female = types.KeyboardButton('femail')
    markup.row(male, female)
    bot.send_message(message.chat.id, text = 'Какого вы пола: ', reply_markup=markup)
    bot.register_next_step_handler(message, get_sex)

def get_sex(message):
    global data
    if message.text == 'male':
        data['sex'] = True
    elif message.text == 'femail':
        data['sex'] = False
    print(data)
    bot.send_message(message.chat.id, text = 'Спасибо')
    id_chat = message.chat.id
    functions.create_new_anket(id_chat, data)
    






    


















# @bot.message_handler(content_types='text')
# def send_photo(message):
#     file_id = 'AgACAgIAAxkBAAICumGtDKcJHYBcREd6QfaOIC_7VS8_AAKotzEbMAZpSQtuCye51sxPAQADAgADeQADIgQ'
#     bot.send_photo(message.chat.id, file_id)

# @bot.message_handler(content_types='text')
# def send_keybord(message):
#     markup = types.InlineKeyboardMarkup()
#     switch_button = types.InlineKeyboardButton(text='Try', switch_inline_query="Telegram")
#     markup.add(switch_button)
#     bot.send_message(message.chat.id, "Нажми на кнопку и перейди на наш сайт.", reply_markup = markup)

# polling
bot.polling(none_stop=True, interval=0)

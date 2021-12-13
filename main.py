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

@bot.message_handler(content_types=['text', 'photo'])
def start_message(message):
    if message.text == '/start':
        id_chat = message.chat.id
        check = functions.check_user_in_db(id_chat)
        if check == False:
        #create new user
            functions.create_new_user(id_chat)
            bot.send_message(message.from_user.id, text='Рад поприветствовать вас впервые.Давай создадим анкету. Как тебя зовут?', reply_markup=types.ReplyKeyboardRemove())
            bot.register_next_step_handler(message, get_name)
        if check == True:
    #bot can say hello use name from database!!!
            bot.send_message(message.from_user.id, text=f'Привет {message.chat.first_name}')
    
def get_name(message):
    global data
    if message.text != None:
        name = message.text
        data['name'] = name
        bot.send_message(message.chat.id, text = 'Введите ваш возраст: ', reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, get_age)
    else:
        bot.send_message(message.chat.id, text = 'Имя только из букав. Введите корректно: ', reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, get_name)
    print(data)
    

def get_age(message):
    global data
    age = message.text
    try:
        age = int(age)
        data['age'] = age
        bot.send_message(message.chat.id, text = 'Кратко опишите себя и свои увлечения: ', reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, get_description)
    except Exception:
        bot.send_message(message.chat.id, text = 'Возраст может состоять только из цифр. Повторите ввод: ')
        bot.register_next_step_handler(message, get_age)
    print(data)
    

def get_description(message):
    global data
    if message.text != None:
        description = message.text
        data['description'] = description
        bot.send_message(message.chat.id, text = 'Прикрепите свое фото: ', reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, get_file)
    else:
        bot.send_message(message.chat.id, text = 'Описание только из букав и цифр. Введите корректно: ', reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, get_description)
    print(data)

def get_file(message):
    global data
    if message.photo != None:
        file_unique_id = message.photo[-1].file_id
        data['file_unique_id'] = file_unique_id
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        male = types.KeyboardButton('male')
        female = types.KeyboardButton('femail')
        markup.row(male, female)
        bot.send_message(message.chat.id, text = 'Какого вы пола: ', reply_markup=markup)
        bot.register_next_step_handler(message, get_sex)
    else:
        bot.send_message(message.chat.id, text = 'Прикрепите пожалуйста только фото.', reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, get_file)
    print(data)

    

def get_sex(message):
    global data
    if message.text == 'male':
        data['sex'] = True
        print(data)
        sex = "Мужской"
        bot.send_message(message.chat.id, text = 'Ваша анкета:')
        bot.send_photo(message.chat.id, data['file_unique_id'], caption=f'{data["name"]}, {sex}\nМне: {data["age"]}\n{data["description"]}')
        id_chat = message.chat.id
        functions.create_new_anket(id_chat, data)
    elif message.text == 'femail':
        data['sex'] = False
        print(data)
        sex = "Мужской"
        bot.send_message(message.chat.id, text = 'Ваша анкета:')
        bot.send_photo(message.chat.id, data['file_unique_id'], caption=f'{data["name"]}, {sex}\nМне: {data["age"]}\n{data["description"]}')
        id_chat = message.chat.id
        functions.create_new_anket(id_chat, data)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        male = types.KeyboardButton('male')
        female = types.KeyboardButton('femail')
        markup.row(male, female)
        bot.send_message(message.chat.id, text = 'Неправильный выбор', reply_markup=markup)
        bot.register_next_step_handler(message, get_sex)

bot.polling(none_stop=True, interval=0)

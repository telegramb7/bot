import os
from dotenv import load_dotenv
import requests
import telebot
import functions
from telebot import types
from flask import Flask, request, jsonify

load_dotenv()

# initialization bot
web_hook = os.getenv('WEB_HOOK')
token = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(token)

server = Flask(__name__)

ANKET_DICT = {}
PK_PARTNER={}

class Anket:
    def __init__(self, name):
        self.name = name
        self.age = None
        self.description =None
        self.file_unique_id = None
        self.sex = None

@bot.message_handler(content_types=['text', 'photo'])
def start_message(message):
    if message.text == '/start':
        id_chat = message.chat.id
        check = functions.check_user_in_db(id_chat)
        if check == False:
        #create new user
            functions.create_new_user(id_chat, message.chat.username)
            bot.send_message(message.from_user.id, text='Рад поприветствовать вас впервые. Обратите внимание, что для корректной работы необходимо иметь username. Если у вас его нет, уставноите в настрйоках телеграм. Давай создадим анкету. Как тебя зовут?', reply_markup=types.ReplyKeyboardRemove())
            bot.register_next_step_handler(message, get_name)
        if check == True:
            username = message.chat.username
            if username == None:
                username = ""
            functions.put_user(message.chat.id, username)
            check_anket = functions.check_anket_in_db(message.chat.id)
            if check_anket == False:
                bot.send_message(message.from_user.id, text= 'Привет у тебя нет Анкеты, давай создадим. Как тебя зовут?', reply_markup=types.ReplyKeyboardRemove())
                bot.register_next_step_handler(message, get_name)
            elif check_anket == True:
                bot.send_message(message.chat.id, text='Давай познакомимся с другими участниками.')
                search(message)
    elif message.text == '/menu':
        username = message.chat.username
        if username == None:
            username = ""
        functions.put_user(message.chat.id, username)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        user_anket = types.KeyboardButton('Ваша анкета📃',)
        find = types.KeyboardButton('Посмотреть другие анкеты👀',)
        pull_anket = types.KeyboardButton('Заполнить свою анкету заново📝',)
        bye = types.KeyboardButton('До следующей встречи👋')
        markup.row(user_anket, find, pull_anket, bye)
        bot.send_message(message.chat.id, text="Меню: ", reply_markup=markup)
        bot.register_next_step_handler(message, main_menu)

    
def get_name(message):
    if message.text != None:

        id_chat = message.chat.id
        name = message.text
        anket = Anket(name)
        ANKET_DICT[id_chat] = anket

        bot.send_message(message.chat.id, text = 'Введите ваш возраст: ', reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, get_age)
    else:
        bot.send_message(message.chat.id, text = 'Имя только из букав. Введите корректно: ', reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, get_name)
    

def get_age(message):
    try:
        id_chat = message.chat.id
        age = message.text
        if not age.isdigit():
            bot.send_message(message.chat.id, text = 'Возраст может состоять только из цифр. Повторите ввод: ')
            bot.register_next_step_handler(message, get_age)
        anket = ANKET_DICT[id_chat]
        anket.age = int(age)
        bot.send_message(message.chat.id, text = 'Кратко опишите себя и свои увлечения: ', reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, get_description)
    except Exception:
        pass
    
def get_description(message):
    id_chat = message.chat.id
    description = message.text
    if message.text != None:
        anket = ANKET_DICT[id_chat]
        anket.description = str(description)
        bot.send_message(message.chat.id, text = 'Прикрепите свое фото: ', reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, get_file)
    else:
        bot.send_message(message.chat.id, text = 'Описание только из букав и цифр. Введите корректно: ', reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, get_description)

def get_file(message):
    id_chat = message.chat.id
    if message.photo != None:
        file_unique_id = message.photo[-1].file_id
        anket = ANKET_DICT[id_chat]
        anket.file_unique_id = str(file_unique_id)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        male = types.KeyboardButton('male')
        female = types.KeyboardButton('femail')
        markup.row(male, female)
        bot.send_message(message.chat.id, text = 'Какого вы пола: ', reply_markup=markup)
        bot.register_next_step_handler(message, get_sex)
    else:
        bot.send_message(message.chat.id, text = 'Прикрепите пожалуйста только фото.', reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, get_file)

def get_sex(message):
    id_chat = message.chat.id
    sex = message.text
    check = functions.check_anket_in_db(id_chat)
    if check == False:
        if message.text == 'male':
            anket = ANKET_DICT[id_chat]
            anket.sex = True
            sex = "Мужской"
            bot.send_message(message.chat.id, text = 'Ваша анкета:')
            bot.send_photo(message.chat.id, anket.file_unique_id, caption=f'{anket.name}, {sex}\nМне: {anket.age}\n{anket.description}')
            functions.create_new_anket(id_chat, ANKET_DICT[id_chat])
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            user_anket = types.KeyboardButton('Ваша анкета📃',)
            find = types.KeyboardButton('Посмотреть другие анкеты👀',)
            pull_anket = types.KeyboardButton('Заполнить свою анкету заново📝',)
            bye = types.KeyboardButton('До следующей встречи👋')
            markup.row(user_anket, find, pull_anket, bye)
            bot.send_message(message.chat.id, text="Меню: ", reply_markup=markup)
            bot.register_next_step_handler(message, main_menu)
        elif message.text == 'femail':
            anket = ANKET_DICT[id_chat]
            anket.sex = False
            sex = "Женский"
            bot.send_message(message.chat.id, text = 'Ваша анкета:')
            bot.send_photo(message.chat.id, anket.file_unique_id, caption=f'{anket.name}, {sex}\nМне: {anket.age}\n{anket.description}', reply_markup=types.ReplyKeyboardRemove())
            functions.create_new_anket(id_chat, ANKET_DICT[id_chat])
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            user_anket = types.KeyboardButton('Ваша анкета📃',)
            find = types.KeyboardButton('Посмотреть другие анкеты👀',)
            pull_anket = types.KeyboardButton('Заполнить свою анкету заново📝',)
            bye = types.KeyboardButton('До следующей встречи👋')
            markup.row(user_anket, find, pull_anket, bye)
            bot.send_message(message.chat.id, text="Меню: ", reply_markup=markup)
            bot.register_next_step_handler(message, main_menu)
    elif check == True:
        if message.text == 'male':
            anket = ANKET_DICT[id_chat]
            anket.sex = True
            sex = "Мужской"
            bot.send_message(message.chat.id, text = 'Ваша анкета:')
            bot.send_photo(message.chat.id, anket.file_unique_id, caption=f'{anket.name}, {sex}\nМне: {anket.age}\n{anket.description}')
            functions.put_anket(message.chat.id, ANKET_DICT[id_chat])
        elif message.text == 'femail':
            anket = ANKET_DICT[id_chat]
            anket.sex = False
            sex = "Женский"
            bot.send_message(message.chat.id, text = 'Ваша анкета:')
            bot.send_photo(message.chat.id, anket.file_unique_id, caption=f'{anket.name}, {sex}\nМне: {anket.age}\n{anket.description}', reply_markup=types.ReplyKeyboardRemove())
            functions.put_anket(message.chat.id, ANKET_DICT[id_chat])
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        user_anket = types.KeyboardButton('Ваша анкета📃',)
        find = types.KeyboardButton('Посмотреть другие анкеты👀',)
        pull_anket = types.KeyboardButton('Заполнить свою анкету заново📝',)
        bye = types.KeyboardButton('До следующей встречи👋')
        markup.row(user_anket, find, pull_anket, bye)
        bot.send_message(message.chat.id, text="Меню: ", reply_markup=markup)
        bot.register_next_step_handler(message, main_menu)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        male = types.KeyboardButton('male')
        female = types.KeyboardButton('femail')
        markup.row(male, female)
        bot.send_message(message.chat.id, text = 'Неправильный выбор', reply_markup=markup)
        bot.register_next_step_handler(message, get_sex)

def search(message):
    search_data = functions.another_anket(message.chat.id)
    # anket = functions.next()
    if search_data == False:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        user_anket = types.KeyboardButton('Ваша анкета📃',)
        find = types.KeyboardButton('Посмотреть другие анкеты👀',)
        pull_anket = types.KeyboardButton('Заполнить свою анкету заново📝',)
        bye = types.KeyboardButton('До следующей встречи👋')
        markup.row(user_anket, find, pull_anket, bye)
        bot.send_message(message.chat.id, text='На сегодня анкеты закончились. Приходите позже. До свидания!', reply_markup=markup)
        bot.register_next_step_handler(message, main_menu)
    elif search_data != False:
        if search_data['sex'] == True:
            sex = "Мужской"
            bot.send_photo(message.chat.id, search_data['file_unique_id'], caption=f'{search_data["name"]}, {sex}\nВозраст: {search_data["age"]}\n{search_data["description"]}')
            PK_PARTNER[message.chat.id] = search_data['user']
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            like = types.KeyboardButton('👍',)
            dislike = types.KeyboardButton('👎',)
            sleep = types.KeyboardButton('👋')
            markup.row(like, dislike, sleep)
            bot.send_message(message.chat.id, text='>', reply_markup=markup)
            bot.register_next_step_handler(message, check_answer)
        elif search_data['sex'] == False:
            sex = "Женский"
            bot.send_photo(message.chat.id, search_data['file_unique_id'], caption=f'{search_data["name"]}, {sex}\nВозраст: {search_data["age"]}\n{search_data["description"]}')
            PK_PARTNER[message.chat.id] = search_data['user']
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            like = types.KeyboardButton('👍',)
            dislike = types.KeyboardButton('👎',)
            sleep = types.KeyboardButton('👋')
            markup.row(like, dislike, sleep)
            bot.send_message(message.chat.id, text='>', reply_markup=markup)
            bot.register_next_step_handler(message, check_answer)


def check_answer(message):
    if message.text == '👋':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        user_anket = types.KeyboardButton('Ваша анкета📃',)
        find = types.KeyboardButton('Посмотреть другие анкеты👀',)
        pull_anket = types.KeyboardButton('Заполнить свою анкету заново📝',)
        bye = types.KeyboardButton('До следующей встречи👋')
        markup.row(user_anket, find, pull_anket, bye)
        bot.send_message(message.chat.id, text = 'До встречи!', reply_markup=markup)
        bot.register_next_step_handler(message, main_menu)
    elif message.text == '👎':
        id_chat = message.chat.id
        id_partner = PK_PARTNER[message.chat.id]
        functions.post_dislike(id_chat, id_partner)
        search(message)
    elif message.text == '👍':
        id_chat = message.chat.id
        id_partner = PK_PARTNER[message.chat.id]
        functions.post_like(id_chat, id_partner)
        match_date = functions.check_match(id_chat, id_partner)
        if match_date == False:
            search(message)
        elif match_date != False:
            if match_date['partner_username'] != "" and match_date["username"] != "":
                bot.send_photo(message.chat.id, match_date['partner_photo'], caption = f'У вас с @{match_date["partner_username"]} совпадение лайков. Вы можете начать общение.')
                bot.send_photo(match_date['partner_id_chat'], match_date['user_photo'], caption = f'У вас с @{match_date["username"]} совпадение лайков. Вы можете начать общение.')
            elif match_date['partner_username'] != "" and match_date["username"] == "":
                bot.send_photo(message.chat.id, match_date['partner_photo'], caption = f'У вас есть совпадение лайков c @{match_date["partner_username"]}, однако у вас не заполнен username и он/она не может начать общение с вами. Проявите инициативу и укажите свой username.')
            elif match_date['partner_username'] == "" and match_date["username"] != "":
                bot.send_photo(match_date['partner_id_chat'], match_date['user_photo'], caption = f'У вас есть совпадение лайков c @{match_date["username"]}, однако у вас не заполнен username и он/она не может начать общение с вами. Проявите инициативу и укажите свой username.')
            elif match_date['partner_username'] == "" and match_date["username"] == "":
                bot.send_message(message.chat.id, text= 'У вас есть совпадение лайков, однако у вас не заполнен username и вы не можете начать общение.')
                bot.send_message(match_date['partner_id_chat'], text='У вас есть совпадение лайков, однако у вас не заполнен username и вы не можете начать общение.')
            search(message)
    elif message.text == "/menu":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        user_anket = types.KeyboardButton('Ваша анкета📃',)
        find = types.KeyboardButton('Посмотреть другие анкеты👀',)
        pull_anket = types.KeyboardButton('Заполнить свою анкету заново📝',)
        bye = types.KeyboardButton('До следующей встречи👋')
        markup.row(user_anket, find, pull_anket, bye)
        bot.send_message(message.chat.id, text="Меню: ", reply_markup=markup)
        bot.register_next_step_handler(message, main_menu)
    else:
        bot.send_message(message.chat.id, text='Неверный выбор. Воспользуйся клавиатурой.')
        bot.register_next_step_handler(message, check_answer)

def main_menu(message):
    if message.text == 'До следующей встречи👋':
        bot.send_message(message.chat.id, text='Возвращайтесь, будем рады видеть вас вновь.', reply_markup=types.ReplyKeyboardRemove())
    elif message.text == 'Заполнить свою анкету заново📝':
        bot.send_message(message.chat.id, text='Введите ваше имя: ')
        bot.register_next_step_handler(message, get_name)
    elif message.text == 'Ваша анкета📃':
        personal_anket = functions.get_personal_data(message.chat.id)
        if personal_anket['sex']== True:
            sex = "Мужской"
        else:
            sex = "Женский"

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        user_anket = types.KeyboardButton('Ваша анкета📃',)
        find = types.KeyboardButton('Посмотреть другие анкеты👀',)
        pull_anket = types.KeyboardButton('Заполнить свою анкету заново📝',)
        bye = types.KeyboardButton('До следующей встречи👋')
        markup.row(user_anket, find, pull_anket, bye)
        bot.send_photo(message.chat.id, personal_anket['file_unique_id'], caption=f'Ваша анкета: {personal_anket["name"]}, {sex}\nМне: {personal_anket["age"]}\n{personal_anket["description"]}', reply_markup=markup)
        bot.send_message(message.chat.id, text="Меню: ")
        bot.register_next_step_handler(message, main_menu)
    elif message.text == 'Посмотреть другие анкеты👀':
        search(message)

# bot.polling(none_stop=True, interval=0)


@server.route('/' + token, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=web_hook + token)
    return "!", 200

# @server.route('/match', methods=['POST'])
# def match(message):
#     first = request.json.get('first')
#     second = request.json.get('second')
#     if first['username'] != "" and second['username'] != "":
#         bot.send_photo(message.chat.id, second['photo'], caption = f'У вас с @{second["username"]} совпадение лайков. Вы можете начать общение.')
#         bot.send_photo(second['id_chat'], first['photo'], caption = f'У вас с @{first["username"]} совпадение лайков. Вы можете начать общение.')
#     elif second['username'] != "" and first["username"] == "":
#         bot.send_photo(message.chat.id, second['photo'], caption = f'У вас есть совпадение лайков c @{second["username"]}, однако у вас не заполнен username и он/она не может начать общение с вами. Проявите инициативу и укажите свой username.')
#     elif second['username'] == "" and first["username"] != "":
#         bot.send_photo(second['id_chat'], first['photo'], caption = f'У вас есть совпадение лайков c @{first["username"]}, однако у вас не заполнен username и он/она не может начать общение с вами. Проявите инициативу и укажите свой username.')
#     elif first['username'] == "" and second["username"] == "":
#         bot.send_message(message.chat.id, text= 'У вас есть совпадение лайков, однако у вас не заполнен username и вы не можете начать общение.')
#         bot.send_message(second['id_chat'], text='У вас есть совпадение лайков, однако у вас не заполнен username и вы не можете начать общение.')
#     print(first)
#     print(second)
#     # import pdb
#     # pdb.set_trace()
#     # bot.send_message(first, text="Test")
#     # bot.send_message(second, text="Test")
#     return jsonify({}), 200

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))

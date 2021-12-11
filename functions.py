from dotenv.main import load_dotenv
import requests 
import os

from telebot import types

load_dotenv()

#links for api
# user_url = 'http://127.0.0.1:8000/user/'
# anket_url = 'http://127.0.0.1:8000/anket/'
# like_url = 'http://127.0.0.1:8000/like/'
# match_url = 'http://127.0.0.1:8000/match/'

#get connect to links
# db_user = requests.get(user_url)
# db_anket = requests.get(anket_url)
# db_like = requests.get(like_url)
# db_match = requests.get(match_url)

#take json from api
# users_json = db_user.json()
# anket_json = db_anket.json()
# like_json = db_like.json()
# match_json = db_match.json()

#Functions for bot
def check_user_in_db(id_chat):

    #get updates users
    user_url = 'http://127.0.0.1:8000/user/'
    db_user = requests.get(user_url)
    users_json = db_user.json()
    
    for i in users_json:
        if id_chat == i['id_chat']:
            return True
    return False

def create_new_user(id_chat):

    #url for post user
    user_url = 'http://127.0.0.1:8000/user/'

    req = requests.post(user_url, data = {'id_chat':id_chat})


def create_new_anket(id_chat, data):
    #prymary key
    pk = None

    #get updates users
    user_url = 'http://127.0.0.1:8000/user/'
    db_user = requests.get(user_url)
    users_json = db_user.json()

    #url for post anket
    anket_url = 'http://127.0.0.1:8000/anket/'

    #take string
    id_chat = str(id_chat)

    for i in users_json:
        if id_chat == i['id_chat']:
            pk = i['id']
    req = requests.post(anket_url, 
        {"name": data['name'],
        "age": int(data['age']),
        "description": data['description'],
        "file_unique_id": data['file_unique_id'],
        "sex": bool(data['sex']),
        "user": pk})


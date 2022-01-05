from dotenv.main import load_dotenv
import requests 
import os
import random

load_dotenv()

#links for api
# user_url = 'http://127.0.0.1:8000/user/'
# anket_url = 'http://127.0.0.1:8000/anket/'
# like_url = 'http://127.0.0.1:8000/like/'
# match_url = 'http://127.0.0.1:8000/match/'
# dislike_url = 'http://127.0.0.1:8000/dislike/'

#get connect to links
# db_user = requests.get(user_url)
# db_anket = requests.get(anket_url)
# db_like = requests.get(like_url)
# db_match = requests.get(match_url)
# db_dislike = requests.get(dislike_url)

#take json from api
# users_json = db_user.json()
# anket_json = db_anket.json()
# like_json = db_like.json()
# match_json = db_match.json()
# dislike_json = db_dislike.json()

#Functions for bot
def check_user_in_db(id_chat):

    user_url = f'http://127.0.0.1:8000/user/?id_chat={id_chat}'
    db_user = requests.get(user_url, headers={'Authorization': 'Api-KeySsNgPPf5.kNsHDONfOY1BYjnYRwbPdgnSkvEsV6E5'})
    users_json = db_user.json()

    if users_json != []:
        return True
    else:
        return False


def create_new_user(id_chat, username=""):

    #url for post user
    user_url = 'http://127.0.0.1:8000/user/'

    req = requests.post(user_url, {'id_chat':id_chat, 'username': username}, headers={'Authorization': 'Api-Key SsNgPPf5.kNsHDONfOY1BYjnYRwbPdgnSkvEsV6E5'})


def create_new_anket(id_chat, data):

    anket_url = 'http://127.0.0.1:8000/anket/'

    user_url = f'http://127.0.0.1:8000/user/?id_chat={id_chat}'
    db_user = requests.get(user_url, headers={'Authorization': 'Api-Key SsNgPPf5.kNsHDONfOY1BYjnYRwbPdgnSkvEsV6E5'})
    users_json = db_user.json()

    pk = users_json[0]['id']

    req = requests.post(anket_url, 
        {"name": data.name,
        "age": data.age,
        "description": data.description,
        "file_unique_id": data.file_unique_id,
        "sex": data.sex,
        "user": pk}, headers={'Authorization': 'Api-Key SsNgPPf5.kNsHDONfOY1BYjnYRwbPdgnSkvEsV6E5'})


def get_personal_data(id_chat):

    user_url = f'http://127.0.0.1:8000/user/?id_chat={id_chat}'
    db_user = requests.get(user_url, headers={'Authorization': 'Api-Key SsNgPPf5.kNsHDONfOY1BYjnYRwbPdgnSkvEsV6E5'})
    users_json = db_user.json()

    pk = users_json[0]['id']

    anket_url = f'http://127.0.0.1:8000/anket/?user={pk}'
    db_anket = requests.get(anket_url, headers={'Authorization': 'Api-Key SsNgPPf5.kNsHDONfOY1BYjnYRwbPdgnSkvEsV6E5'})
    anket_json = db_anket.json()
    
    return {
            'name':anket_json[0]['name'],
            'age':anket_json[0]['age'],
            'description':anket_json[0]['description'],
            'file_unique_id':anket_json[0]['file_unique_id'],
            'sex':anket_json[0]['sex']
            }

def check_anket_in_db(id_chat):

    user_url = f'http://127.0.0.1:8000/user/?id_chat={id_chat}'
    db_user = requests.get(user_url, headers={'Authorization': 'Api-Key SsNgPPf5.kNsHDONfOY1BYjnYRwbPdgnSkvEsV6E5'})
    users_json = db_user.json()

    pk = users_json[0]['id']

    anket_url = f'http://127.0.0.1:8000/anket/?user={pk}'
    db_anket = requests.get(anket_url, headers={'Authorization': 'Api-Key SsNgPPf5.kNsHDONfOY1BYjnYRwbPdgnSkvEsV6E5'})
    anket_json = db_anket.json()

    if anket_json != []:
        return True
    else:
        return False


def another_anket(id_chat):
    
    all_pk = []
    all_dis = []

    user_url = f'http://127.0.0.1:8000/user/?id_chat={id_chat}'
    db_user = requests.get(user_url, headers={'Authorization': 'Api-Key SsNgPPf5.kNsHDONfOY1BYjnYRwbPdgnSkvEsV6E5'})
    users_json = db_user.json()

    pk = users_json[0]['id']

    anket_url = 'http://127.0.0.1:8000/anket/'
    db_anket = requests.get(anket_url, headers={'Authorization': 'Api-Key SsNgPPf5.kNsHDONfOY1BYjnYRwbPdgnSkvEsV6E5'})
    anket_json = db_anket.json()

    dislike_url = f'http://127.0.0.1:8000/dislike/?who={pk}'
    db_dislike = requests.get(dislike_url, headers={'Authorization': 'Api-Key SsNgPPf5.kNsHDONfOY1BYjnYRwbPdgnSkvEsV6E5'})
    dislike_json = db_dislike.json()

    for i in anket_json:
        all_pk.append(i['user'])
    
    all_pk.remove(int(pk))

    if dislike_json != []:
        for i in dislike_json:
            all_dis.append(i["whom_dislike"])
            all_pk.remove(i["whom_dislike"])

    like_url = 'http://127.0.0.1:8000/like/'
    db_like = requests.get(like_url)
    like_json = db_like.json()

    for i in like_json:
        if pk == i['user']:
           all_pk.remove(i['partner']) 

    if all_pk != []:
        for i in all_pk:
            url_anket = f'http://127.0.0.1:8000/anket/?user={i}'
            user_db = requests.get(url_anket, headers={'Authorization': 'Api-Key SsNgPPf5.kNsHDONfOY1BYjnYRwbPdgnSkvEsV6E5'})
            json_anket = user_db.json()
        
            return {
                'user':json_anket[0]['user'],
                'name':json_anket[0]['name'],
                'age':json_anket[0]['age'],
                'description':json_anket[0]['description'],
                'file_unique_id':json_anket[0]['file_unique_id'],
                'sex':json_anket[0]['sex']
            }
    else:
        if all_dis == []:
            return False
        else:
            ran_ch = random.choice(all_dis)
            url_anket = f'http://127.0.0.1:8000/anket/?user={ran_ch}'
            user_db = requests.get(url_anket, headers={'Authorization': 'Api-Key SsNgPPf5.kNsHDONfOY1BYjnYRwbPdgnSkvEsV6E5'})
            json_anket = user_db.json()
            return {
                'user':json_anket[0]['user'],
                'name':json_anket[0]['name'],
                'age':json_anket[0]['age'],
                'description':json_anket[0]['description'],
                'file_unique_id':json_anket[0]['file_unique_id'],
                'sex':json_anket[0]['sex']
                }

def post_like(id_chat, id_partner):

    user_url = f'http://127.0.0.1:8000/user/?id_chat={id_chat}'
    db_user = requests.get(user_url, headers={'Authorization': 'Api-Key SsNgPPf5.kNsHDONfOY1BYjnYRwbPdgnSkvEsV6E5'})
    users_json = db_user.json()

    pk = users_json[0]['id']
    id_partner = int(id_partner) # this can remove

    dislike_url = f'http://127.0.0.1:8000/dislike/?who={pk}'
    db_dislike = requests.get(dislike_url, headers={'Authorization': 'Api-Key SsNgPPf5.kNsHDONfOY1BYjnYRwbPdgnSkvEsV6E5'})
    dislike_json = db_dislike.json()

    for i in dislike_json:
        if i['whom_dislike'] == id_partner:
            dislike_url = f'http://127.0.0.1:8000/dislike/{i["id"]}'
            req = requests.delete(dislike_url)
    
    like_url = 'http://127.0.0.1:8000/like/'
    req = requests.post(like_url,
    {
    "user": pk,
    "partner": id_partner
        }, headers={'Authorization': 'Api-Key SsNgPPf5.kNsHDONfOY1BYjnYRwbPdgnSkvEsV6E5'})
    

def post_dislike(id_chat, id_partner):

    dislike_url = 'http://127.0.0.1:8000/dislike/'

    user_url = f'http://127.0.0.1:8000/user/?id_chat={id_chat}'
    db_user = requests.get(user_url, headers={'Authorization': 'Api-Key SsNgPPf5.kNsHDONfOY1BYjnYRwbPdgnSkvEsV6E5'})
    users_json = db_user.json()

    pk = users_json[0]['id']
    id_partner = int(id_partner)

    dislike_who = f'http://127.0.0.1:8000/dislike/?who={pk}&whom={id_partner}'
    dislike_who_db = requests.get(dislike_who, headers={'Authorization': 'Api-Key SsNgPPf5.kNsHDONfOY1BYjnYRwbPdgnSkvEsV6E5'})
    dislike_who_json = dislike_who_db.json()

    if dislike_who_json == []:
        req = requests.post(dislike_url,
        {
            "who_dislike": pk,
            "whom_dislike": id_partner
        }, headers={'Authorization': 'Api-Key SsNgPPf5.kNsHDONfOY1BYjnYRwbPdgnSkvEsV6E5'})


def check_match(id_chat, id_partner):

    #find pk id_chat

    user_url = f'http://127.0.0.1:8000/user/?id_chat={id_chat}'
    db_user = requests.get(user_url, headers={'Authorization': 'Api-Key SsNgPPf5.kNsHDONfOY1BYjnYRwbPdgnSkvEsV6E5'})
    users_json = db_user.json()

    pk = users_json[0]['id']
    username = users_json[0]['username']

    user_url = f'http://127.0.0.1:8000/user/?id_user={id_partner}'
    db_user = requests.get(user_url, headers={'Authorization': 'Api-Key SsNgPPf5.kNsHDONfOY1BYjnYRwbPdgnSkvEsV6E5'})
    users_json = db_user.json()

    partner_id_chat = users_json[0]['id_chat']
    partner_username = users_json[0]['username']

    user_like_url = f'http://127.0.0.1:8000/like/?user={pk}&partner={id_partner}'
    partner_like_url = f'http://127.0.0.1:8000/like/?user={id_partner}&partner={pk}'

    user_db_like = requests.get(user_like_url)
    partner_db_like = requests.get(partner_like_url)

    user_like_json = user_db_like.json()
    partner_like_json = partner_db_like.json()

    user_anket_url = f"http://127.0.0.1:8000/anket/?user={pk}"
    partner_anket_url = f"http://127.0.0.1:8000/anket/?user={id_partner}"
    db_user_anket = requests.get(user_anket_url, headers={'Authorization': 'Api-Key SsNgPPf5.kNsHDONfOY1BYjnYRwbPdgnSkvEsV6E5'})
    db_partner_anket = requests.get(partner_anket_url, headers={'Authorization': 'Api-Key SsNgPPf5.kNsHDONfOY1BYjnYRwbPdgnSkvEsV6E5'})
    user_anket_json = db_user_anket.json()
    partner_anket_json = db_partner_anket.json()

    if user_like_json != [] and partner_like_json != []:
        return {'username':username,
        'partner_username':partner_username,
        'partner_id_chat':partner_id_chat,
        'user_photo': user_anket_json[0]['file_unique_id'],
        'partner_photo':partner_anket_json[0]['file_unique_id']}
        
    else:
        return False

def put_anket(id_chat, data):

    user_url = f'http://127.0.0.1:8000/user/?id_chat={id_chat}'
    db_user = requests.get(user_url, headers={'Authorization': 'Api-Key SsNgPPf5.kNsHDONfOY1BYjnYRwbPdgnSkvEsV6E5'})
    users_json = db_user.json()

    pk = users_json[0]['id']

    personal_anket_url = f'http://127.0.0.1:8000/anket/?user={pk}'
    db_personal_anket = requests.get(personal_anket_url, headers={'Authorization': 'Api-Key SsNgPPf5.kNsHDONfOY1BYjnYRwbPdgnSkvEsV6E5'})
    personal_anket_json = db_personal_anket.json()

    id_anket = personal_anket_json[0]['id']

    anket_url = f'http://127.0.0.1:8000/anket/{id_anket}/'

    req = requests.put(anket_url, 
        {"name": data.name,
        "age": data.age,
        "description": data.description,
        "file_unique_id": data.file_unique_id,
        "sex": data.sex,
        "user": pk}, headers={'Authorization': 'Api-Key SsNgPPf5.kNsHDONfOY1BYjnYRwbPdgnSkvEsV6E5'})

def put_user(id_chat, username=''):

    user_url = f'http://127.0.0.1:8000/user/?id_chat={id_chat}'
    db_user = requests.get(user_url, headers={'Authorization': 'Api-Key SsNgPPf5.kNsHDONfOY1BYjnYRwbPdgnSkvEsV6E5'})
    users_json = db_user.json()
    pk = users_json[0]['id']

    user_url = f'http://127.0.0.1:8000/user/{pk}/'

    req = requests.put(user_url, {'id_chat':id_chat, 'username': username}, headers={'Authorization': 'Api-Key SsNgPPf5.kNsHDONfOY1BYjnYRwbPdgnSkvEsV6E5'})

from dotenv import load_dotenv
import requests 
import os
import random

load_dotenv()
API_KEY = os.getenv('API_KEY')

url = 'https://familiar-api.herokuapp.com'
# url = 'http://127.0.0.1:8000'


#Functions for bot
def check_user_in_db(id_chat):
    """
    A function that checks if a User with the received id_chat is in the database.

    If User is in the database returns True.
    If User is not in the database returns False.

    GOOD
    """

    user_url = f'{url}/user/?id_chat={id_chat}'
    db_user = requests.get(user_url, headers={'Authorization': 'Api-Key '+ API_KEY})
    users_json = db_user.json()

    if users_json != []:
        return True
    else:
        return False

def create_new_user(id_chat, username=""):
    """
    Function for creating a new User in the database.

    The mandatory argument is id_chat.
    The username can be empty. 

    GOOD
    """

    user_url = f'{url}/user/'

    req = requests.post(user_url, {'id_chat':id_chat, 'username': username}, headers={'Authorization': 'Api-Key '+ API_KEY})


def create_new_anket(id_chat, data):
    """
    Function to create a Profile for a specific User.

    Id_chat is needed to determine the User ID.
    Data is a special class containing the information to be collected for the profile.

    GOOD
    """

    anket_url = f'{url}/anket/'

    user_url = f'{url}/user/?id_chat={id_chat}'
    db_user = requests.get(user_url, headers={'Authorization': 'Api-Key '+ API_KEY})
    users_json = db_user.json()

    pk = users_json[0]['id']

    req = requests.post(anket_url, 
        {"name": data.name,
        "age": data.age,
        "description": data.description,
        "file_unique_id": data.file_unique_id,
        "sex": data.sex,
        "user": pk}, 
        headers={'Authorization': 'Api-Key '+ API_KEY})

def get_personal_data(id_chat):
    """
    Function for retrieving stored Anket data of a specific User.

    Id_chat is required to obtain a User ID.

    GOOD
    """

    anket_url = f'{url}/anket/me/'
    db_anket = requests.get(anket_url, json={'id_chat':id_chat}, headers={'Authorization': 'Api-Key '+ API_KEY})
    anket_json = db_anket.json()
    
    return {
            'name':anket_json['name'],
            'age':anket_json['age'],
            'description':anket_json['description'],
            'file_unique_id':anket_json['file_unique_id'],
            'sex':anket_json['sex']
            }

def check_anket_in_db(id_chat):
    """
    Checking the availability of Anket for a particular User.

    Id_chat is required to obtain a User ID.

    GOOD
    """

    anket_url = f'{url}/anket/me/'
    db_anket = requests.get(anket_url, json={'id_chat':id_chat}, headers={'Authorization': 'Api-Key '+ API_KEY})
    if db_anket.status_code == 200:
        return True
    else:
        return False

def another_anket(id_chat):
    """
    A function that returns another user's profile.
    The selection is currently implemented as follows:
    A list of all profiles is generated.
    A list of all dislikes is generated.
    User's profile will be deleted from the list.
    Unsuitable profiles are deleted from the list.
    The first questionnaire is returned from the remaining list.
    If the list is empty, return the questionnaire from the list of those not liked. 

    Id_chat is required to obtain a User ID.

    GOOD
    """

    anket_url = f'{url}/anket/?id_chat={id_chat}'
    db_anket = requests.get(anket_url, headers={'Authorization': 'Api-Key '+ API_KEY})
    ankets_json = db_anket.json()

    if ankets_json != []:
        for anket_json in ankets_json:
            return {
                'user':anket_json['user'],
                'name':anket_json['name'],
                'age':anket_json['age'],
                'description':anket_json['description'],
                'file_unique_id':anket_json['file_unique_id'],
                'sex':anket_json['sex']
            }
    elif ankets_json == []:
        dislike_url = f'{url}/dislike/?id_chat={id_chat}'
        db_dislike = requests.get(dislike_url, headers={'Authorization': 'Api-Key '+ API_KEY})
        dislike_json =db_dislike.json()
        if dislike_json == []:
            return False
        elif dislike_json != []:
            pk = dislike_json[0]['whom_dislike']
            user_url = f'{url}/user/?id_user={pk}'
            db_user = requests.get(user_url, headers={'Authorization': 'Api-Key '+ API_KEY})
            users_json = db_user.json()
            chat_id = users_json[0]['id_chat']
    
            anket_for_url = f'{url}/anket/me/'
            db_for_anket = requests.get(anket_for_url, json={'id_chat':chat_id}, headers={'Authorization': 'Api-Key '+ API_KEY})
            anket_for_json = db_for_anket.json()
            return {
                'user':anket_for_json['user'],
                'name':anket_for_json['name'],
                'age':anket_for_json['age'],
                'description':anket_for_json['description'],
                'file_unique_id':anket_for_json['file_unique_id'],
                'sex':anket_for_json['sex']
            }

# def next():
#     ankets = another_anket()
#     for anket in ankets:
#         yield anket


def post_like(id_chat, id_partner):
    """
    Function for posting Like.

    Id_chat is required to obtain a User ID.
    Id_partner is the id of the user to rate. 

    GOOD
    """

    user_url = f'{url}/user/?id_chat={id_chat}'
    db_user = requests.get(user_url, headers={'Authorization': 'Api-Key '+ API_KEY})
    users_json = db_user.json()

    pk = users_json[0]['id']
    id_partner = int(id_partner) 

    dislike_url = f'{url}/dislike/?who={pk}'
    db_dislike = requests.get(dislike_url, headers={'Authorization': 'Api-Key '+ API_KEY})
    dislike_json = db_dislike.json()

    for i in dislike_json:
        if i['whom_dislike'] == id_partner:
            dislike_url = f'{url}/dislike/{i["id"]}'
            req = requests.delete(dislike_url, headers={'Authorization': 'Api-Key '+ API_KEY})
    
    like_url = f'{url}/like/'
    req = requests.post(like_url,
    {
    "user": pk,
    "partner": id_partner
        }, headers={'Authorization': 'Api-Key '+ API_KEY})
    

def post_dislike(id_chat, id_partner):
    """
    Function for posting Dislike.

    Id_chat is required to obtain a User ID.
    Id_partner is the id of the user to rate. 

    GOOD
    """

    dislike_url = f'{url}/dislike/'

    user_url = f'{url}/user/?id_chat={id_chat}'
    db_user = requests.get(user_url, headers={'Authorization': 'Api-Key '+ API_KEY})
    users_json = db_user.json()

    pk = users_json[0]['id']
    id_partner = int(id_partner)

    req = requests.post(dislike_url,
        {
            "who_dislike": pk,
            "whom_dislike": id_partner
        }, headers={'Authorization': 'Api-Key '+ API_KEY})

def check_match(id_chat, id_partner):
    """
    Function for checking matches.

    Id_chat is required to obtain a User ID.
    Id_partner is the ID of the user we are checking for a match with.

    GOOD
    """

    user_url = f'{url}/user/?id_chat={id_chat}'
    db_user = requests.get(user_url, headers={'Authorization': 'Api-Key '+ API_KEY})
    users_json = db_user.json()

    pk = users_json[0]['id']
    username = users_json[0]['username']

    user_url = f'{url}/user/?id_user={id_partner}'
    db_user = requests.get(user_url, headers={'Authorization': 'Api-Key '+ API_KEY})
    users_json = db_user.json()

    partner_id_chat = users_json[0]['id_chat']
    partner_username = users_json[0]['username']

    user_like_url = f'{url}/like/?user={pk}&partner={id_partner}'
    partner_like_url = f'{url}/like/?user={id_partner}&partner={pk}'

    user_db_like = requests.get(user_like_url, headers={'Authorization': 'Api-Key '+ API_KEY})
    partner_db_like = requests.get(partner_like_url, headers={'Authorization': 'Api-Key '+ API_KEY})

    user_like_json = user_db_like.json()
    partner_like_json = partner_db_like.json()

    user_anket_url = f"{url}/anket/me/"
    partner_anket_url = f"{url}/anket/me/"
    db_user_anket = requests.get(user_anket_url,json={'id_chat':id_chat}, headers={'Authorization': 'Api-Key '+ API_KEY})
    db_partner_anket = requests.get(partner_anket_url, json={'id_chat':partner_id_chat}, headers={'Authorization': 'Api-Key '+ API_KEY})
    user_anket_json = db_user_anket.json()
    partner_anket_json = db_partner_anket.json()

    if user_like_json != [] and partner_like_json != []:
        return {'username':username,
        'partner_username':partner_username,
        'partner_id_chat':partner_id_chat,
        'user_photo': user_anket_json['file_unique_id'],
        'partner_photo':partner_anket_json['file_unique_id']}
        
    else:
        return False

def put_anket(id_chat, data):
    """
    Function for updating Anket data.

    Id_chat is required to obtain a User ID.
    Data is a special class containing the information to be collected for the profile.

    GOOD
    """

    user_url = f'{url}/user/?id_chat={id_chat}'
    db_user = requests.get(user_url, headers={'Authorization': 'Api-Key '+ API_KEY})
    users_json = db_user.json()

    pk = users_json[0]['id']

    anket_url = f'{url}/anket/me/'
    db_anket = requests.get(anket_url, json={'id_chat':id_chat}, headers={'Authorization': 'Api-Key '+ API_KEY})
    anket_json = db_anket.json()

    id_anket = anket_json['id']

    anket_url = f'{url}/anket/{id_anket}/'

    req = requests.put(anket_url, 
        {"name": data.name,
        "age": data.age,
        "description": data.description,
        "file_unique_id": data.file_unique_id,
        "sex": data.sex,
        "user": pk}, headers={'Authorization': 'Api-Key '+ API_KEY})

def put_user(id_chat, username=''):
    """
    Function for updating User data.
    For an ideal scenario, the User Name is required. This function updates the User at key moments, in particular if a username is added.

    GOOD
    """

    user_url = f'{url}/user/?id_chat={id_chat}'
    db_user = requests.get(user_url, headers={'Authorization': 'Api-Key '+ API_KEY})
    users_json = db_user.json()
    pk = users_json[0]['id']

    user_url = f'{url}/user/{pk}/'

    req = requests.put(user_url, {'id_chat':id_chat, 'username': username}, headers={'Authorization': 'Api-Key '+ API_KEY})


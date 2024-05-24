import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

credential = credentials.ApplicationDefault()
conf = {'projectId': 'raki-todo-task'}
firebase_admin.initialize_app(credential, conf)

db = firestore.client()


def get_users():
    return db.collection('users').get()

def get_user(user_id):
    return db.collection('users').document(user_id).get()

def get_todos(user_id):
    return db.collection('users').document(user_id).collection('todos').get()

def put_user(user_dto):
    user = db.collection('users').document(user_dto.username)
    user.set({'password': user_dto.password})
    
def put_todo(user_id, description):
    documents = db.collection('users').document(user_id).collection('todos')
    documents.add({'description': description})
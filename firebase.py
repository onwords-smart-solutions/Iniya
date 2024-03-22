from fastapi import HTTPException
import firebase_admin
from firebase_admin import credentials, initialize_app, db

cred = credentials.Certificate('OST.json')

firebase_admin.initialize_app(cred, { 'databaseURL': 'https://smart-things-ab7d2-default-rtdb.firebaseio.com/'})
 
def get_data_from_firebase(path):
    ref = db.reference(path)
    ref = ref.get()
    return ref
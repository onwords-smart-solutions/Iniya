from fastapi import HTTPException
import firebase_admin
from firebase_admin import credentials, initialize_app, auth, db
from firebase_admin import db

cred = credentials.Certificate('smart-things-ab7d2-firebase-adminsdk-92yxa-9904898922.json')

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://smart-things-ab7d2-default-rtdb.firebaseio.com/'
})

def authenticate_user(email: str):
    try:
        user = auth.get_user_by_email(email)
        return {"localId": user.uid}
    except auth.UserNotFoundError:
        return{"localId":"User not found"}
    except Exception as e:
        raise ValueError("Authentication failed: " + str(e))
 
def get_data_from_firebase(path):
    ref = db.reference(path)
    ref = ref.get()
    return ref
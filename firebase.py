import firebase_admin
from firebase_admin import credentials
from firebase_admin import db




# Path to your service account's private key file
cred = credentials.Certificate('smart-things-ab7d2-firebase-adminsdk-92yxa-9904898922.json')

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://smart-things-ab7d2-default-rtdb.firebaseio.com/'
})

def get_data_from_firebase(path):
    ref = db.reference(path)
    ref = ref.get()
    return ref
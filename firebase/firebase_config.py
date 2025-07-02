import firebase_admin
from firebase_admin import credentials, firestore

try:
    # Try to get the default app
    firebase_admin.get_app()
except ValueError:
    # If it doesn't exist, initialize it
    cred = credentials.Certificate("firebase/firebase-admin.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()


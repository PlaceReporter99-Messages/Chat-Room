import argon2
import hashlib
import firebase_admin
from firebase_admin import firestore
app = firebase_admin.initialize_app()
db = firestore.client()
true = True
false = False
null = None
def verify_login(username: str, password: str):
    hash_function = lambda x: argon2.hash_password(x, salt=bytes(hashlib.sha3_256(x).hexdigest(), 'utf-8')).decode('utf-8') # We use the Keccak hash to determine the salt.
    try:
        return db.collection("logins").document(username.lower()).get().to_dict()["password_hash"] == hash_function(bytes(password, 'utf-8'))
    except:
        return false
import argon2
import hashlib
from pymongo import MongoClient
import bson
import os

def get_password_hash(db: MongoClient, username: str):
    return db.login.find_one({"username": username})["password_hash"]

def sign(db: MongoClient, sender: str, recipient: str, message: str):
    return hashlib.sha3_256(bytes(get_password_hash(db, sender) + get_password_hash(db, recipient) + message, 'utf-8')).hexdigest()

def check_signature(db: MongoClient, message_id: bson.objectid.ObjectId):
    message = db.message.find_one({'_id', message_id})
    return message["signature"] == sign(db, message["sender"], message["recipient"], message["message"])

def hash_function(password: bytes):
    return argon2.hash_password(password, salt=bytes(hashlib.sha3_256(password).hexdigest(), 'utf-8')).decode('utf-8') # We use the Keccak hash to determine the salt.

def verify_login(db: MongoClient, username: str, password: str):
    try:
        return get_password_hash(db, username) == hash_function(bytes(password, 'utf-8'))
    except:
        return False
    
def verify_server_login(db: MongoClient, password: str):
    return verify_login(db, "(server)", password)

def create_account(db: MongoClient, username: str, password: str):
    if db.login.find_one({'username': username}):
        return False
    else:
        db.login.insert_one({'username': username, 'password_hash': hash_function(bytes(password, 'utf-8'))})
        return True
    
def send_message(db: MongoClient, sender: str, recipient: str, message: str):
    signature = sign(db, sender, recipient, message)
    db.message.insert_one({"message": message, "sender": sender, "recipient": recipient, "signature": signature})
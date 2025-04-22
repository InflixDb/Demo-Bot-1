from pymongo import MongoClient
from config import MONGO_URL

client = MongoClient(MONGO_URL)
db = client.invite_bot

channels = db.channels  # stores channel info
users = db.users        # tracks users
requests = db.requests  # anime requests

def add_user(user_id):
    users.update_one({"_id": user_id}, {"$set": {}}, upsert=True)

def register_channel(chat_id, title):
    channels.update_one({"_id": chat_id}, {"$set": {"title": title}}, upsert=True)

def remove_channel(chat_id):
    channels.delete_one({"_id": chat_id})

def get_channels():
    return list(channels.find())

def save_request(user_id, anime):
    requests.insert_one({"user_id": user_id, "anime": anime})

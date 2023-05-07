from pymongo import MongoClient
from helpers.env import load_env


def saveCode(email, code):
    client = MongoClient(load_env("APP_MONGODB_URL"))
    db = client["djangoMFA"]
    codes_collection = db["codes"]

    codes_collection.insert_one({
        "email": email,
        "code": code,
    })

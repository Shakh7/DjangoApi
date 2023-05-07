from datetime import datetime
import random
import string

import requests
from pymongo import MongoClient
from helpers.env import load_env
from helpers.telegram import send_auth_one_time_code


class MongoDB:
    def __init__(self):
        self.client = MongoClient(load_env("APP_MONGODB_URL"))
        self.db = self.client["djangoMFA"]
        self.codes_collection = self.db["codes"]
        self.random_code = None
        self.due_to = None
        self.inserted_code_id = None

    def generateRandomCode(self):
        self.random_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        print("random_code", self.random_code)

    def saveCode(self, email, code):
        current_time = datetime.now()
        inserted_code = self.codes_collection.insert_one({
            "email": email,
            "code": code,
            "date_issued": current_time
        })
        self.inserted_code_id = inserted_code.inserted_id
        return code

    def findCode(self, email, code):
        self.codes_collection.find_one({
            "email": email,
            "code": code
        })

    def performMFA(self, email, access_token):
        self.generateRandomCode()
        code = self.saveCode(email, self.random_code, access_token)
        send_auth_one_time_code(code)
        return code

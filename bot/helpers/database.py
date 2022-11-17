from pymongo import MongoClient
from pymongo.errors import PyMongoError

from bot.logging import LOGGER
from bot.config import SUDO_USERS, DATABASE_URL

class DatabaseHelper:

    def __init__(self):
        self.__err = False
        self.__client = None
        self.__db = None
        self.__collection = None
        self.__connect()

    def __connect(self):
        try:
            self.__client = MongoClient(DATABASE_URL)
            self.__db = self.__client['MFBot']
            self.__collection = self.__db['users']
        except PyMongoError as err:
            LOGGER(__name__).error(err)
            self.__err = True

    def auth_user(self, user_id: int):
        if self.__err:
            return
        self.__collection.insert_one({"user_id": user_id})
        self.__client.close()
        return '<b><i>Successfully added to Sudo Users List!</i></b>'

    def unauth_user(self, user_id: int):
        if self.__err:
            return
        self.__collection.delete_many({"user_id": user_id})
        self.__client.close()
        return '<b><i>Successfully removed to Sudo Users List!</i></b>'

    def load_users(self):
        if self.__err:
            return
        users = self.__collection.find().sort("user_id")
        for user in users:
            SUDO_USERS.add(user["user_id"])
        self.__client.close()

if DATABASE_URL is not None:
    DatabaseHelper().load_users()
from motor.motor_asyncio import AsyncIOMotorClient


class Mongo:
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if Mongo.__instance == None:
            Mongo()
        return Mongo.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if Mongo.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            Mongo.__instance = self

    async def connect(self, url, db_name):
        self.connection = AsyncIOMotorClient(url)
        self.db = self.connection[db_name]

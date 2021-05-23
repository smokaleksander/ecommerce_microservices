import asyncio
from nats.aio.client import Client as NATS
from stan.aio.client import Client as STAN
import json
import random
import string


class NatsWrapper:
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if NatsWrapper.__instance == None:
            NatsWrapper()
        return NatsWrapper.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if NatsWrapper.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            NatsWrapper.__instance = self

    async def connect(self):
        self.nc = NATS()
        conn = await self.nc.connect("nats-srv:4222")
        self.client_id = ''.join(random.choices(
            string.ascii_uppercase + string.digits, k=8))
        self.sc = STAN()
        # print(self.nc.is_connected)
        await self.sc.connect(cluster_id="ecom", client_id=self.client_id, nats=self.nc)

    async def disconnect(self):
        await self.sc.close()
        await self.nc.close()
        self.sc = None
        self.nc = None

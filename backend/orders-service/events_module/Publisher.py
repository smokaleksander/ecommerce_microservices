import asyncio
from nats.aio.client import Client as NATS
from stan.aio.client import Client as STAN
import json
import random
import string
from .NatsWrapper import NatsWrapper


class Publisher:

    def __init__(self, subject):
        self.subject = subject

    async def publish(self, data):

        client = NatsWrapper.getInstance()
        data = json.dumps(data)
        await client.sc.publish(subject=self.subject, payload=bytes(data, 'utf-8'))

        # await sc.close()
        # await nc.close()

import asyncio
from typing import Dict
import json
import random
import string
from .NatsWrapper import NatsWrapper


class Publisher:

    def __init__(self, subject):
        self.subject = subject

    async def ack_handler(ack):
        print("Received ack: {}".format(ack.guid))

    async def publish(self, data: Dict):

        client = NatsWrapper.getInstance()
        print(type(data))
        print(data)
        await client.sc.publish(subject=self.subject.value, payload=bytes(data, 'UTF-8'), ack_handler=self.ack_handler)
        print(self.subject.value)
        # await sc.close()
        # await nc.close()

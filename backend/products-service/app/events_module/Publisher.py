import asyncio
from typing import Dict
import json
import random
import string
from .NatsWrapper import NatsWrapper


class Publisher:

    def __init__(self, subject):
        self.subject = subject

    async def ack_handler():
        print("Received ack")

    async def publish(self, data):

        client = NatsWrapper.getInstance()
        await client.sc.publish(subject=self.subject.value, payload=bytes(data, 'UTF-8'), ack_handler=self.ack_handler)
        # await sc.close()
        # await nc.close()

import asyncio
import json
from .NatsWrapper import NatsWrapper
from .EventType import EventType


class Publisher:

    def __init__(self, subject: EventType):
        self.subject = subject

    async def publish(self, data: json):

        client = NatsWrapper.getInstance()
        await client.sc.publish(subject=self.subject.value, payload=bytes(data, 'UTF-8'))

        # await sc.close()
        # await nc.close()

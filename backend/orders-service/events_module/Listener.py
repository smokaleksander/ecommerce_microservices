import asyncio
import json
from .EventType import EventType
from .NatsWrapper import NatsWrapper
from config import settings
from fastapi import Request


class Listener:
    ack_wait_time = 30  # seconds

    def __init__(self, subject, on_receive_func):
        self.subject = subject
        self.on_receive_func = on_receive_func
        self.queue_group_name = settings.APP_NAME

    async def listen(self):
        client = NatsWrapper.getInstance()
        # callback on msg
        #future = asyncio.Future(loop=asyncio.get_event_loop())

        async def cb(msg):
            # nonlocal future
            print("Received a message (seq={}): {}".format(msg.seq, msg.data))
            await client.sc.ack(msg)
            obj = msg.data.decode('UTF-8')
            obj = json.loads(obj)
            await self.on_receive_func(Request, obj)

        # Subscribe to get all messages since beginning.
        sub = await client.sc.subscribe(
            subject=self.subject.value,
            deliver_all_available=True,
            durable_name=self.queue_group_name,
            cb=cb,
            queue=self.queue_group_name,
            manual_acks=True,
            ack_wait=self.ack_wait_time)

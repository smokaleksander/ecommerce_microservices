import asyncio
from nats.aio.client import Client as NATS
from stan.aio.client import Client as STAN
import json
from abc import ABC, abstractmethod


class Listener:
    ack_wait_time = 5*1000

    def __init__(self, subject, queue_group_name):
        self.subject = subject
        self.queue_group_name = queue_group_name
        self.client_id = os.urandom(4)

    async def run(self, loop):
        # Use borrowed connection for NATS then mount NATS Streaming
        # client on top.
        nc = NATS()
        await nc.connect("127.0.0.1:4222", io_loop=loop)

        # Start session with NATS Streaming cluster.
        sc = STAN()
        await sc.connect(cluster_id="ecom", client_id=self.client_id, nats=nc)

        # # Synchronous Publisher, does not return until an ack
        # # has been received from NATS Streaming.
        total_messages = 0
        future = asyncio.Future(loop=loop)

        # callback on msg
        async def cb(msg):
            nonlocal future
            nonlocal total_messages
            nonlocal sc
            print("Received a message (seq={}): {}".format(msg.seq, msg.data))
            await sc.ack(msg)
            # total_messages += 1
            # if total_messages >= 2:
            #     future.set_result(None)

        # Subscribe to get all messages since beginning.
        sub = await sc.subscribe(
            subject=self.subject,
            deliver_all_available=True,
            durable_name=self.queue_group_name,
            cb=cb,
            queue=self.queue_group_name,
            manual_acks=True,
            ack_wait=self.ack_wait_time)
        await asyncio.wait_for(future, timeout=None)

        # # Stop receiving messages
        #
        await sub.unsubscribe()

        # # Close NATS Streaming session
        await sc.close()

        # # We are using a NATS borrowed connection so we need to close manually.
        await nc.close()

    def listen(self, *args, **kwargs):
        loop = asyncio.get_event_loop()
        # loop.run_until_complete(run(loop))
        asyncio.gather(self.run(loop))
        loop.run_forever()
        # loop.close()


if __name__ == '__main__':
    ls = Listener(subject="products:created",
                  queue_group_name='products-service',
                  client_id='cl1')
    ls.listen()

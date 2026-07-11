import asyncio
import orjson

from nats.aio.client import Client # type: ignore

from events import EventEnvelope


class EventBus:

    def __init__(self):

        self.nc = Client()

    async def connect(self):

        await self.nc.connect(
            servers=["nats://nats:4222"]
        )

    async def publish(

        self,

        topic,

        event: EventEnvelope,

    ):

        await self.nc.publish(

            topic,

            orjson.dumps(event.__dict__),
        )

    async def subscribe(

        self,

        topic,

        callback,

    ):

        await self.nc.subscribe(

            topic,

            cb=callback,
        )

    async def flush(self):

        await self.nc.flush()

    async def close(self):

        await self.nc.drain()

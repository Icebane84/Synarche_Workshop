import asyncio

from packages.common.event_bus import EventBus


class RuntimeContext:

    def __init__(self):

        self.bus = EventBus()

    def initialize(self):

        asyncio.run(

            self.bus.connect()

        )

    def shutdown(self):

        asyncio.run(

            self.bus.close()

        )

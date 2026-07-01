import asyncio

from packages.common.event_bus import EventBus

from .container import PlatformContainer


def build_container():

    bus = EventBus()

    asyncio.run(

        bus.connect()

    )

    return PlatformContainer(

        event_bus=bus

    )

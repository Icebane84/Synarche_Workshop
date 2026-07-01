import asyncio

import parser_pb2
import parser_pb2_grpc

from parser_engine import ParserEngine

from packages.common.event_bus import EventBus
from packages.common.event_factory import create_event
from packages.common.event_types import EventType
from packages.common.topics import Topic


class ParserService(parser_pb2_grpc.ParserAPIServicer):

    def __init__(self):

        self.engine = ParserEngine()

        self.bus = EventBus()

        asyncio.run(self.bus.connect())

    def _publish(self, event):

        asyncio.run(

            self.bus.publish(

                Topic.PARSER,

                event,

            )

        )

    def Parse(self, request, context):

        #
        # Parse incoming specification
        #

        ast = self.engine.parse(request.source)

        #
        # Publish completion event
        #

        event = create_event(

            source="parser-service",

            event_type=EventType.PARSER_COMPLETED,

            payload={

                "source_hash": ast["source_hash"],

                "length": ast["length"],

                "ast_version": ast["ast_version"],

            },
        )

        self._publish(event)

        #
        # Return serialized AST
        #

        return parser_pb2.AST(

            json=self.engine.serialize(ast)

        )

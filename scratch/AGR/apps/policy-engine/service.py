import asyncio

import policy_pb2
import policy_pb2_grpc

from config import settings
from evaluator import PolicyEvaluator

from packages.common.event_bus import EventBus
from packages.common.event_factory import create_event
from packages.common.event_types import EventType
from packages.common.topics import Topic


class PolicyService(
    policy_pb2_grpc.PolicyAPIServicer
):

    def __init__(self):

        self.engine = PolicyEvaluator(settings)

        self.bus = EventBus()

        asyncio.run(self.bus.connect())

    def _publish(self, event):

        asyncio.run(

            self.bus.publish(

                Topic.POLICY,

                event,

            )

        )

    def Evaluate(self, request, context):

        (
            allow,
            quarantined,
            violations,
        ) = self.engine.evaluate(request)

        #
        # Publish policy decision
        #

        event = create_event(

            source="policy-engine",

            event_type=(

                EventType.POLICY_APPROVED

                if allow

                else EventType.POLICY_DENIED

            ),

            payload={

                "allow": allow,

                "quarantined": quarantined,

                "violations": violations,

                "spiffe_id": request.identity.spiffe_id,

            },
        )

        self._publish(event)

        #
        # Return decision
        #

        return policy_pb2.PolicyDecision(

            allow=allow,

            quarantined=quarantined,

            violations=violations,

        )

import policy_pb2
import policy_pb2_grpc

from evaluator import PolicyEvaluator
from config import settings


class PolicyService(
    policy_pb2_grpc.PolicyAPIServicer
):

    def __init__(self):

        self.engine = PolicyEvaluator(settings)

    def Evaluate(self, request, context):

        allow, quarantined, violations = (
            self.engine.evaluate(request)
        )

        return policy_pb2.PolicyDecision(

            allow=allow,

            quarantined=quarantined,

            violations=violations,
        )
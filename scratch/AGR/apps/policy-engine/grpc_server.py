from concurrent import futures

import grpc

import policy_pb2_grpc

from service import PolicyService

from config import settings


def serve():

    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=16)
    )

    policy_pb2_grpc.add_PolicyAPIServicer_to_server(
        PolicyService(),
        server,
    )

    server.add_insecure_port(
        f"[::]:{settings.grpc_port}"
    )

    server.start()

    server.wait_for_termination()
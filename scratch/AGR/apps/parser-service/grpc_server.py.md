from concurrent import futures

import grpc

import parser_pb2_grpc

from service import ParserService

from config import settings


def serve():

    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=16)
    )

    parser_pb2_grpc.add_ParserAPIServicer_to_server(
        ParserService(),
        server,
    )

    server.add_insecure_port(
        f"[::]:{settings.grpc_port}"
    )

    server.start()

    server.wait_for_termination()
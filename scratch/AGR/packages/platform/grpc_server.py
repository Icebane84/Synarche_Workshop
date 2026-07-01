from concurrent import futures

import grpc


class GrpcRuntime:

    def __init__(

        self,

        servicer,

        register,

        port,

        workers=16,

    ):

        self.server = grpc.server(

            futures.ThreadPoolExecutor(

                max_workers=workers

            )

        )

        register(

            servicer,

            self.server,

        )

        self.server.add_insecure_port(

            f"[::]:{port}"

        )

    def start(self):

        self.server.start()

    def wait(self):

        self.server.wait_for_termination()

    def stop(self):

        self.server.stop(5)

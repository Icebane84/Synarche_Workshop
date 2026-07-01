import threading

import uvicorn

from .grpc_server import GrpcRuntime

from .http_server import create_runtime_http

from .lifecycle import RuntimeContext

from .signals import install_shutdown


class ServiceRuntime:

    def __init__(

        self,

        name,

        grpc_servicer,

        grpc_register,

        grpc_port,

        http_port,

    ):

        self.context = RuntimeContext()

        self.context.initialize()

        self.grpc = GrpcRuntime(

            servicer=grpc_servicer,

            register=grpc_register,

            port=grpc_port,

        )

        self.http = create_runtime_http(

            name

        )

        self.http_port = http_port

        install_shutdown(self)

    def start(self):

        grpc_thread = threading.Thread(

            target=self.grpc.wait,

            daemon=True,

        )

        self.grpc.start()

        grpc_thread.start()

        uvicorn.run(

            self.http,

            host="0.0.0.0",

            port=self.http_port,

        )

    def shutdown(self):

        self.grpc.stop()

        self.context.shutdown()

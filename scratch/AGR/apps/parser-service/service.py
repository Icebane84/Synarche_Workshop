from parser_engine import ParserEngine

# generated protobuf imports
import parser_pb2
import parser_pb2_grpc


class ParserService(parser_pb2_grpc.ParserAPIServicer):

    def __init__(self):

        self.engine = ParserEngine()

    def Parse(self, request, context):

        ast = self.engine.parse(request.source)

        return parser_pb2.AST(
            json=self.engine.serialize(ast)
        )
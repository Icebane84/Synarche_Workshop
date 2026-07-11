import json

import validation_pb2
import validation_pb2_grpc

from analyzer import StaticAnalyzer


class ValidationService(
    validation_pb2_grpc.ValidationAPIServicer
):

    def __init__(self):
        self.analyzer = StaticAnalyzer()

    def Validate(self, request, context):

        ast = json.loads(request.ast_json)

        findings = self.analyzer.analyze(ast)

        return validation_pb2.ValidationResult(
            passed=len(findings) == 0,
            findings=findings,
        )
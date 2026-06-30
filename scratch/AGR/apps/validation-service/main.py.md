from packages.common.service import create_http_app

app = create_http_app("Validation Service")

#
# gRPC startup follows the same pattern
# as Parser Service and Policy Engine.
#
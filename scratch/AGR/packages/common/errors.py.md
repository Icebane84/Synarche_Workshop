class AGRException(Exception):
    pass


class PolicyViolation(AGRException):
    pass


class ValidationFailure(AGRException):
    pass


class GraphError(AGRException):
    pass
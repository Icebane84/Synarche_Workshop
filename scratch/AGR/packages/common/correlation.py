import contextvars
import uuid

_trace = contextvars.ContextVar(
    "trace_id",
    default=None,
)


def current_trace():

    trace = _trace.get()

    if trace is None:

        trace = str(uuid.uuid4())

        _trace.set(trace)

    return trace


def set_trace(trace):

    _trace.set(trace)

from events import EventEnvelope

from correlation import current_trace


def create_event(

    source,

    event_type,

    payload,

):

    event = EventEnvelope()

    event.source = source

    event.event_type = event_type

    event.trace_id = current_trace()

    event.payload = payload

    return event

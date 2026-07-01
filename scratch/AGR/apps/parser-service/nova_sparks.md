Update Parser Service

When parsing succeeds:

event = create_event(

    source="parser-service",

    event_type=EventType.PARSER_COMPLETED,

    payload={

        "hash": ast["source_hash"],

        "length": ast["length"],

    },

)

await event_bus.publish(

    Topic.PARSER,

    event,

)

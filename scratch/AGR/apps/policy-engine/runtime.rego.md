package architecture.governance.runtime

default allow := false

allow if {
    startswith(
        input.identity.spiffe_id,
        "spiffe://agr.internal/ns/"
    )

    input.telemetry.system_coherence_metric >= 0.90
}

quarantined if {
    input.telemetry.system_coherence_metric < 0.90
}
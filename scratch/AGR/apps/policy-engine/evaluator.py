class PolicyEvaluator:

    def __init__(self, settings):

        self.threshold = settings.scm_threshold

    def evaluate(self, request):

        violations = []

        allow = True

        if not request.identity.spiffe_id.startswith(
            "spiffe://agr.internal/ns/"
        ):

            allow = False

            violations.append("INVALID_SPIFFE_ID")

        if (
            request.metrics.system_coherence_metric
            < self.threshold
        ):

            allow = False

            violations.append("SYSTEM_COHERENCE_TOO_LOW")

        quarantined = (
            request.metrics.system_coherence_metric
            < self.threshold
        )

        return allow, quarantined, violations
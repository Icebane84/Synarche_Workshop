class TopologyValidator:

    def validate_node_degree(

        self,

        incoming,

        outgoing,

    ):

        #
        # Specification:
        #
        # Nodes with zero degree
        # fail validation.
        #

        return (incoming + outgoing) > 0
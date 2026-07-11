from topology import TopologyValidator

from postgres_repository import (

    PostgresGraphRepository,

)

from config import settings


class GraphService:

    def __init__(self):

        self.repository = (

            PostgresGraphRepository(

                settings

            )
        )

        self.validator = (

            TopologyValidator()

        )
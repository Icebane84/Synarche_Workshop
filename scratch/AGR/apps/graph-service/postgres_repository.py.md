import psycopg

from repository import GraphRepository


class PostgresGraphRepository(GraphRepository):

    def __init__(self, settings):

        self.connection = psycopg.connect(

            host=settings.postgres_host,

            port=settings.postgres_port,

            dbname=settings.postgres_database,

            user=settings.postgres_user,

            password=settings.postgres_password,
        )

    def add_node(self, node):

        #
        # Apache AGE implementation
        # will go here.
        #

        pass

    def add_edge(self, edge):

        pass

    def get_node(self, node_id):

        pass

    def neighbors(self, node_id):

        return []

    def topology_health(self):

        return {
            "healthy": True
        }
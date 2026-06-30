from abc import ABC, abstractmethod


class GraphRepository(ABC):

    @abstractmethod
    def add_node(self, node):
        ...

    @abstractmethod
    def add_edge(self, edge):
        ...

    @abstractmethod
    def get_node(self, node_id):
        ...

    @abstractmethod
    def neighbors(self, node_id):
        ...

    @abstractmethod
    def topology_health(self):
        ...
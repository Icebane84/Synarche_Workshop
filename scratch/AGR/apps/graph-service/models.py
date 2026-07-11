from dataclasses import dataclass


@dataclass
class Node:

    id: str

    type: str

    properties: dict


@dataclass
class Edge:

    source: str

    target: str

    relationship: str

    properties: dict
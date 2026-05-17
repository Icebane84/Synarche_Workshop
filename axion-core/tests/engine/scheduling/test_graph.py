import pytest
from engine.scheduling.compiled_graph import CompiledGraph

class MockTask:
    def __init__(self, name, deps=None):
        self.name = name
        self.deps = deps or []

def test_compiled_graph_layering():
    # Arrange
    t1 = MockTask("task_1")
    t2 = MockTask("task_2", deps=["task_1"])
    t3 = MockTask("task_3", deps=["task_1"])
    t4 = MockTask("task_4", deps=["task_2", "task_3"])
    
    graph = CompiledGraph([t1, t2, t3, t4])
    
    # Act
    graph.build()
    
    # Assert
    assert len(graph.layers) == 3
    assert [t.name for t in graph.layers[0]] == ["task_1"]
    # Task 2 and 3 should be in layer 1, sorted alphabetically
    assert [t.name for t in graph.layers[1]] == ["task_2", "task_3"]
    assert [t.name for t in graph.layers[2]] == ["task_4"]

def test_compiled_graph_cycle_detection():
    # Arrange
    t1 = MockTask("task_1", deps=["task_2"])
    t2 = MockTask("task_2", deps=["task_1"])
    
    graph = CompiledGraph([t1, t2])
    
    # Act & Assert
    with pytest.raises(RuntimeError, match="Cycle detected"):
        graph.build()

def test_compiled_graph_empty():
    graph = CompiledGraph([])
    graph.build()
    assert len(graph.layers) == 0

import pytest
from engine.scheduling.compiled_graph import CompiledGraph
from engine.scheduling.layered_scheduler import LayeredScheduler

class MockTask:
    def __init__(self, name, deps=None):
        self.name = name
        self.deps = deps or []
        self.executed = False

    def run(self, context):
        self.executed = True
        context["log"].append(self.name)

def test_layered_scheduler_execution():
    # Arrange
    t1 = MockTask("t1")
    t2 = MockTask("t2", deps=["t1"])
    t3 = MockTask("t3", deps=["t1"])
    
    graph = CompiledGraph([t1, t2, t3])
    graph.build()
    
    scheduler = LayeredScheduler(graph)
    context = {"log": []}
    
    # Act
    scheduler.execute(context)
    
    # Assert
    assert t1.executed
    assert t2.executed
    assert t3.executed
    # t1 must be first
    assert context["log"][0] == "t1"
    # t2 and t3 should be in next layer, sorted alphabetically
    assert context["log"][1:] == ["t2", "t3"]

def test_layered_scheduler_no_graph():
    scheduler = LayeredScheduler(None)
    with pytest.raises(ValueError, match="No graph provided"):
        scheduler.execute({})

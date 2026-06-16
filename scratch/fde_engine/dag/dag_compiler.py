class DAGCompiler:
    def __init__(self, systems):
        self.systems = systems

    def compile_layers(self):
        return [[s] for s in sorted(self.systems, key=lambda x: x.execution_index)]

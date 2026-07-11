class StaticAnalyzer:

    def analyze(self, ast: dict):

        findings = []

        if "nodes" not in ast:
            findings.append("AST_MISSING_NODES")

        if "edges" not in ast:
            findings.append("AST_MISSING_EDGES")

        if len(ast.get("nodes", [])) == 0:
            findings.append("EMPTY_NODE_GRAPH")

        return findings
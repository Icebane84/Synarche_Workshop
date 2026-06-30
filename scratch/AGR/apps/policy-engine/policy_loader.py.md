from pathlib import Path


class PolicyLoader:

    def __init__(self, directory):

        self.directory = Path(directory)

    def load(self):

        policies = {}

        for file in self.directory.glob("*.rego"):

            policies[file.name] = file.read_text()

        return policies
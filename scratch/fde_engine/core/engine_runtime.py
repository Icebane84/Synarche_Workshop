
class EngineRuntime:
    def __init__(self, world, scheduler):
        self.world = world
        self.scheduler = scheduler

    def tick(self, inputs: dict):
        self.world.current_inputs = inputs
        self.scheduler.run_frame(self.world)
        self.world.frame += 1

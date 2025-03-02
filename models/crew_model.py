class CrewModel:
    def __init__(self, name="", description="", agents=None, tasks=None, process="sequential", verbose=True):
        self.name = name
        self.description = description
        self.agents = agents or []
        self.tasks = tasks or []
        self.process = process
        self.verbose = verbose
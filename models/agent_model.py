class AgentModel:
    def __init__(self, name="", role="", goal="", backstory="", verbose=True, allow_delegation=False, tools=None):
        self.name = name
        self.role = role
        self.goal = goal
        self.backstory = backstory
        self.verbose = verbose
        self.allow_delegation = allow_delegation
        self.tools = tools or []
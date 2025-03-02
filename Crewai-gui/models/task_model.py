class TaskModel:
    def __init__(self, name="", description="", expected_output="", agent="", output_file=""):
        self.name = name
        self.description = description
        self.expected_output = expected_output
        self.agent = agent
        self.output_file = output_file
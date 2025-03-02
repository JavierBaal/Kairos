# CrewAI GUI

<p align="center">
  <img src="docs/images/logo.png" alt="CrewAI GUI Logo" width="200"/>
</p>

## Overview

CrewAI GUI is a graphical user interface for the [CrewAI framework](https://github.com/joaomdmoura/crewAI), designed to simplify the creation, management, and execution of AI agent crews. This tool allows users to visually define agents, tasks, and workflows without writing code, making the powerful CrewAI framework accessible to a wider audience.

## Features

- **Agent Management**: Create, edit, and delete AI agents with customizable roles, goals, and backstories
- **Task Management**: Define tasks with descriptions, expected outputs, and assign them to specific agents
- **Crew Configuration**: Organize agents and tasks into crews with different process types
- **Real-time Execution**: Run your crews directly from the GUI and see the output in real-time
- **Configuration Export**: Save agent, task, and crew configurations as YAML files compatible with CrewAI
- **Intuitive Interface**: User-friendly tabbed interface for managing different aspects of your AI crews

## Screenshots

<p align="center">
  <img src="docs/images/screenshot_agents.png" alt="Agents Tab" width="45%"/>
  <img src="docs/images/screenshot_crews.png" alt="Crews Tab" width="45%"/>
</p>

## Installation

### Prerequisites

- Python 3.8 or higher
- PyQt6
- CrewAI and its dependencies

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/CrewAI-GUI.git
cd CrewAI-GUI

CrewAI-GUI/
├── config/                 # Configuration files directory
│   ├── agents.yaml         # Saved agent configurations
│   ├── tasks.yaml          # Saved task configurations
│   └── crews.yaml          # Saved crew configurations
├── docs/                   # Documentation
│   └── images/             # Screenshots and images
├── models/                 # Data models
│   ├── agent_model.py      # Agent data structure
│   ├── task_model.py       # Task data structure
│   └── crew_model.py       # Crew data structure
├── scripts/                # Generated scripts for execution
├── ui/                     # User interface components
│   ├── agent_panel.py      # Agent management panel
│   ├── task_panel.py       # Task management panel
│   ├── crew_panel.py       # Crew management panel
│   └── execution_dialog.py # Execution output dialog
├── .gitignore              # Git ignore file
├── LICENSE                 # License file
├── main.py                 # Application entry point
├── README.md               # Project documentation
└── requirements.txt        # Python dependencies
```plaintext
```

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch ( git checkout -b feature/amazing-feature )
3. Commit your changes ( git commit -m 'Add some amazing feature' )
4. Push to the branch ( git push origin feature/amazing-feature )
5. Open a Pull Request
## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments
- CrewAI - The framework that inspired this GUI
- PyQt6 - The GUI framework used

```
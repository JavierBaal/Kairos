from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QTextEdit, QPushButton, QListWidget, QFormLayout, 
    QCheckBox, QMessageBox, QInputDialog, QComboBox
)
import yaml
import os
import sys

# Add the parent directory to sys.path to make the models module accessible
sys.path.append('/Users/vanguardhive/Desktop/TRABAJOS/SALA-CREATIVA/CrewalAIGui')
from models.agent_model import AgentModel

class AgentPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.agents = {}
        self.init_ui()
        
    def init_ui(self):
        layout = QHBoxLayout(self)
        
        # Left panel - Agent list
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        
        self.agent_list = QListWidget()
        self.agent_list.itemClicked.connect(self.load_agent)
        
        left_layout.addWidget(QLabel("Agents:"))
        left_layout.addWidget(self.agent_list)
        
        button_layout = QHBoxLayout()
        self.add_button = QPushButton("Add Agent")
        self.delete_button = QPushButton("Delete Agent")
        self.add_button.clicked.connect(self.add_agent)
        self.delete_button.clicked.connect(self.delete_agent)
        
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.delete_button)
        left_layout.addLayout(button_layout)
        
        # Right panel - Agent details
        right_panel = QWidget()
        self.right_layout = QFormLayout(right_panel)
        
        self.agent_name = QLineEdit()
        self.agent_role = QTextEdit()
        self.agent_goal = QTextEdit()
        self.agent_backstory = QTextEdit()
        self.agent_verbose = QCheckBox("Verbose")
        self.agent_verbose.setChecked(True)
        self.agent_delegation = QCheckBox("Allow Delegation")
        self.agent_tools = QComboBox()
        
        # Add common tools
        self.agent_tools.addItem("")
        self.agent_tools.addItem("SerperDevTool")
        self.agent_tools.addItem("WebBrowserTool")
        self.agent_tools.addItem("FileReadTool")
        self.agent_tools.addItem("FileWriteTool")
        
        self.right_layout.addRow("Name:", self.agent_name)
        self.right_layout.addRow("Role:", self.agent_role)
        self.right_layout.addRow("Goal:", self.agent_goal)
        self.right_layout.addRow("Backstory:", self.agent_backstory)
        self.right_layout.addRow("Tools:", self.agent_tools)
        self.right_layout.addRow(self.agent_verbose)
        self.right_layout.addRow(self.agent_delegation)
        
        # Save button
        self.save_agent_button = QPushButton("Save Agent")
        self.save_agent_button.clicked.connect(self.save_current_agent)
        self.right_layout.addRow(self.save_agent_button)
        
        # Add panels to main layout
        layout.addWidget(left_panel, 1)
        layout.addWidget(right_panel, 2)
        
        # Load existing agents
        self.load_agents()
        
    def add_agent(self):
        name, ok = QInputDialog.getText(self, "Add Agent", "Agent Name:")
        if ok and name:
            if name in self.agents:
                QMessageBox.warning(self, "Warning", "Agent with this name already exists")
                return
                
            self.agents[name] = AgentModel(name=name)
            self.agent_list.addItem(name)
            self.clear_form()
            self.agent_name.setText(name)
    
    def delete_agent(self):
        current_item = self.agent_list.currentItem()
        if current_item:
            name = current_item.text()
            confirm = QMessageBox.question(
                self, "Confirm Deletion", 
                f"Are you sure you want to delete agent '{name}'?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if confirm == QMessageBox.StandardButton.Yes:
                self.agents.pop(name, None)
                self.agent_list.takeItem(self.agent_list.row(current_item))
                self.clear_form()
    
    def load_agent(self, item):
        name = item.text()
        if name in self.agents:
            agent = self.agents[name]
            self.agent_name.setText(agent.name)
            self.agent_role.setText(agent.role)
            self.agent_goal.setText(agent.goal)
            self.agent_backstory.setText(agent.backstory)
            self.agent_verbose.setChecked(agent.verbose)
            self.agent_delegation.setChecked(agent.allow_delegation)
            
            # Set tool if available
            if agent.tools and len(agent.tools) > 0:
                tool_name = agent.tools[0]
                index = self.agent_tools.findText(tool_name)
                if index >= 0:
                    self.agent_tools.setCurrentIndex(index)
    
    def save_current_agent(self):
        name = self.agent_name.text()
        if not name:
            QMessageBox.warning(self, "Warning", "Agent name cannot be empty")
            return
            
        tool = self.agent_tools.currentText()
        tools_list = [tool] if tool else []
        
        agent = AgentModel(
            name=name,
            role=self.agent_role.toPlainText(),
            goal=self.agent_goal.toPlainText(),
            backstory=self.agent_backstory.toPlainText(),
            verbose=self.agent_verbose.isChecked(),
            allow_delegation=self.agent_delegation.isChecked(),
            tools=tools_list
        )
        
        # Update or add agent
        self.agents[name] = agent
        
        # Update list if it's a new agent
        found = False
        for i in range(self.agent_list.count()):
            if self.agent_list.item(i).text() == name:
                found = True
                break
        
        if not found:
            self.agent_list.addItem(name)
            
        QMessageBox.information(self, "Success", f"Agent '{name}' saved successfully")
    
    def clear_form(self):
        self.agent_name.clear()
        self.agent_role.clear()
        self.agent_goal.clear()
        self.agent_backstory.clear()
        self.agent_verbose.setChecked(True)
        self.agent_delegation.setChecked(False)
        self.agent_tools.setCurrentIndex(0)
    
    def save_agents(self):
        # Convert agents to YAML format
        agents_dict = {}
        for name, agent in self.agents.items():
            agents_dict[name] = {
                "role": agent.role,
                "goal": agent.goal,
                "backstory": agent.backstory,
                "verbose": agent.verbose,
                "allow_delegation": agent.allow_delegation,
                "tools": agent.tools
            }
        
        # Ensure config directory exists
        os.makedirs("config", exist_ok=True)
        
        # Save to YAML file
        with open("config/agents.yaml", "w") as f:
            yaml.dump(agents_dict, f)
    
    def load_agents(self):
        try:
            if os.path.exists("config/agents.yaml"):
                with open("config/agents.yaml", "r") as f:
                    agents_dict = yaml.safe_load(f)
                
                if agents_dict:
                    self.agents = {}
                    self.agent_list.clear()
                    
                    for name, data in agents_dict.items():
                        agent = AgentModel(
                            name=name,
                            role=data.get("role", ""),
                            goal=data.get("goal", ""),
                            backstory=data.get("backstory", ""),
                            verbose=data.get("verbose", True),
                            allow_delegation=data.get("allow_delegation", False),
                            tools=data.get("tools", [])
                        )
                        
                        self.agents[name] = agent
                        self.agent_list.addItem(name)
        except Exception as e:
            QMessageBox.warning(self, "Warning", f"Failed to load agents: {str(e)}")
    
    def get_agents(self):
        return self.agents
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QTextEdit, QPushButton, QListWidget, QFormLayout, 
    QComboBox, QMessageBox, QInputDialog, QCheckBox,
    QListWidgetItem, QDialog, QDialogButtonBox
)
from PyQt6.QtCore import Qt
import yaml
import os
import sys
import subprocess
import time  # Add this import

# Ensure models module is accessible
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from models.crew_model import CrewModel

class SelectItemsDialog(QDialog):
    def __init__(self, title, items, selected_items=None):
        super().__init__()
        self.setWindowTitle(title)
        self.resize(400, 300)
        
        layout = QVBoxLayout(self)
        
        self.list_widget = QListWidget()
        self.list_widget.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        
        # Add items to the list
        for item_name in items:
            list_item = QListWidgetItem(item_name)
            self.list_widget.addItem(list_item)
            
            # Select items that were previously selected
            if selected_items and item_name in selected_items:
                list_item.setSelected(True)
        
        layout.addWidget(self.list_widget)
        
        # Add buttons
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
    
    def get_selected_items(self):
        selected = []
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            if item.isSelected():
                selected.append(item.text())
        return selected

class CrewPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.crews = {}
        self.agents = {}
        self.tasks = {}
        self.init_ui()
        
    def init_ui(self):
        layout = QHBoxLayout(self)
        
        # Left panel - Crew list
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        
        self.crew_list = QListWidget()
        self.crew_list.itemClicked.connect(self.load_crew)
        
        left_layout.addWidget(QLabel("Crews:"))
        left_layout.addWidget(self.crew_list)
        
        button_layout = QHBoxLayout()
        self.add_button = QPushButton("Add Crew")
        self.delete_button = QPushButton("Delete Crew")
        self.add_button.clicked.connect(self.add_crew)
        self.delete_button.clicked.connect(self.delete_crew)
        
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.delete_button)
        left_layout.addLayout(button_layout)
        
        # Right panel - Crew details
        right_panel = QWidget()
        self.right_layout = QFormLayout(right_panel)
        
        self.crew_name = QLineEdit()
        self.crew_description = QTextEdit()
        
        self.crew_agents_button = QPushButton("Select Agents")
        self.crew_agents_button.clicked.connect(self.select_agents)
        self.crew_agents_label = QLabel("No agents selected")
        
        self.crew_tasks_button = QPushButton("Select Tasks")
        self.crew_tasks_button.clicked.connect(self.select_tasks)
        self.crew_tasks_label = QLabel("No tasks selected")
        
        self.crew_process = QComboBox()
        self.crew_process.addItems(["sequential", "hierarchical"])
        
        self.crew_verbose = QCheckBox("Verbose")
        self.crew_verbose.setChecked(True)
        
        self.right_layout.addRow("Name:", self.crew_name)
        self.right_layout.addRow("Description:", self.crew_description)
        self.right_layout.addRow("Agents:", self.crew_agents_button)
        self.right_layout.addRow("", self.crew_agents_label)
        self.right_layout.addRow("Tasks:", self.crew_tasks_button)
        self.right_layout.addRow("", self.crew_tasks_label)
        self.right_layout.addRow("Process:", self.crew_process)
        self.right_layout.addRow(self.crew_verbose)
        
        # Save and Run buttons
        button_layout = QHBoxLayout()
        self.save_crew_button = QPushButton("Save Crew")
        self.run_crew_button = QPushButton("Run Crew")
        self.save_crew_button.clicked.connect(self.save_current_crew)
        self.run_crew_button.clicked.connect(self.run_crew)
        
        button_layout.addWidget(self.save_crew_button)
        button_layout.addWidget(self.run_crew_button)
        self.right_layout.addRow(button_layout)
        
        # Add panels to main layout
        layout.addWidget(left_panel, 1)
        layout.addWidget(right_panel, 2)
        
        # Load existing crews
        self.load_crews()
        
    def add_crew(self):
        name, ok = QInputDialog.getText(self, "Add Crew", "Crew Name:")
        if ok and name:
            if name in self.crews:
                QMessageBox.warning(self, "Warning", "Crew with this name already exists")
                return
                
            self.crews[name] = CrewModel(name=name)
            self.crew_list.addItem(name)
            self.clear_form()
            self.crew_name.setText(name)
    
    def delete_crew(self):
        current_item = self.crew_list.currentItem()
        if current_item:
            name = current_item.text()
            confirm = QMessageBox.question(
                self, "Confirm Deletion", 
                f"Are you sure you want to delete crew '{name}'?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if confirm == QMessageBox.StandardButton.Yes:
                self.crews.pop(name, None)
                self.crew_list.takeItem(self.crew_list.row(current_item))
                self.clear_form()
    
    def load_crew(self, item):
        name = item.text()
        if name in self.crews:
            crew = self.crews[name]
            self.crew_name.setText(crew.name)
            self.crew_description.setText(crew.description)
            
            # Update agents label
            if crew.agents:
                self.crew_agents_label.setText(", ".join(crew.agents))
            else:
                self.crew_agents_label.setText("No agents selected")
            
            # Update tasks label
            if crew.tasks:
                self.crew_tasks_label.setText(", ".join(crew.tasks))
            else:
                self.crew_tasks_label.setText("No tasks selected")
            
            # Set process
            index = self.crew_process.findText(crew.process)
            if index >= 0:
                self.crew_process.setCurrentIndex(index)
            
            # Set verbose
            self.crew_verbose.setChecked(crew.verbose)
    
    def select_agents(self):
        if not self.agents:
            QMessageBox.warning(self, "Warning", "No agents available. Please create agents first.")
            return
        
        current_crew = self.get_current_crew_data()
        dialog = SelectItemsDialog("Select Agents", self.agents.keys(), current_crew.agents)
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            selected_agents = dialog.get_selected_items()
            current_crew.agents = selected_agents
            
            if selected_agents:
                self.crew_agents_label.setText(", ".join(selected_agents))
            else:
                self.crew_agents_label.setText("No agents selected")
    
    def select_tasks(self):
        if not self.tasks:
            QMessageBox.warning(self, "Warning", "No tasks available. Please create tasks first.")
            return
        
        current_crew = self.get_current_crew_data()
        dialog = SelectItemsDialog("Select Tasks", self.tasks.keys(), current_crew.tasks)
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            selected_tasks = dialog.get_selected_items()
            current_crew.tasks = selected_tasks
            
            if selected_tasks:
                self.crew_tasks_label.setText(", ".join(selected_tasks))
            else:
                self.crew_tasks_label.setText("No tasks selected")
    
    def get_current_crew_data(self):
        name = self.crew_name.text()
        if name in self.crews:
            return self.crews[name]
        return CrewModel(name=name)
    
    def save_current_crew(self):
        name = self.crew_name.text()
        if not name:
            QMessageBox.warning(self, "Warning", "Crew name cannot be empty")
            return
        
        current_crew = self.get_current_crew_data()
        current_crew.description = self.crew_description.toPlainText()
        current_crew.process = self.crew_process.currentText()
        current_crew.verbose = self.crew_verbose.isChecked()
        
        # Update or add crew
        self.crews[name] = current_crew
        
        # Update list if it's a new crew
        found = False
        for i in range(self.crew_list.count()):
            if self.crew_list.item(i).text() == name:
                found = True
                break
        
        if not found:
            self.crew_list.addItem(name)
            
        QMessageBox.information(self, "Success", f"Crew '{name}' saved successfully")
    
    def clear_form(self):
        self.crew_name.clear()
        self.crew_description.clear()
        self.crew_agents_label.setText("No agents selected")
        self.crew_tasks_label.setText("No tasks selected")
        self.crew_process.setCurrentIndex(0)
        self.crew_verbose.setChecked(True)
    
    def update_agents(self, agents):
        self.agents = agents
    
    def update_tasks(self, tasks):
        self.tasks = tasks
    
    def save_crews(self):
        # Convert crews to YAML format
        crews_dict = {}
        for name, crew in self.crews.items():
            crews_dict[name] = {
                "description": crew.description,
                "agents": crew.agents,
                "tasks": crew.tasks,
                "process": crew.process,
                "verbose": crew.verbose
            }
        
        # Ensure config directory exists
        os.makedirs("config", exist_ok=True)
        
        # Save to YAML file
        with open("config/crews.yaml", "w") as f:
            yaml.dump(crews_dict, f)
    
    def load_crews(self):
        try:
            if os.path.exists("config/crews.yaml"):
                with open("config/crews.yaml", "r") as f:
                    crews_dict = yaml.safe_load(f)
                
                if crews_dict:
                    self.crews = {}
                    self.crew_list.clear()
                    
                    for name, data in crews_dict.items():
                        crew = CrewModel(
                            name=name,
                            description=data.get("description", ""),
                            agents=data.get("agents", []),
                            tasks=data.get("tasks", []),
                            process=data.get("process", "sequential"),
                            verbose=data.get("verbose", True)
                        )
                        
                        self.crews[name] = crew
                        self.crew_list.addItem(name)
        except Exception as e:
            QMessageBox.warning(self, "Warning", f"Failed to load crews: {str(e)}")
    
    def run_crew(self):
        current_item = self.crew_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "Warning", "Please select a crew to run")
            return
        
        name = current_item.text()
        if name not in self.crews:
            QMessageBox.warning(self, "Warning", f"Crew '{name}' not found")
            return
        
        crew = self.crews[name]
        
        if not crew.agents:
            QMessageBox.warning(self, "Warning", "No agents selected for this crew")
            return
        
        if not crew.tasks:
            QMessageBox.warning(self, "Warning", "No tasks selected for this crew")
            return
        
        # Generate the script
        script_path = self.generate_crew_script(crew)
        if not script_path:
            return
        
        # Create and show execution dialog
        from ui.execution_dialog import ExecutionDialog
        dialog = ExecutionDialog(f"Running Crew: {name}")
        dialog.execute_script(script_path)
        dialog.exec()
    
    def generate_crew_script(self, crew):
        """Generate a Python script to run the crew using CrewAI"""
        try:
            # Create scripts directory if it doesn't exist
            scripts_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts")
            os.makedirs(scripts_dir, exist_ok=True)
            
            # Create a unique script file
            script_path = os.path.join(scripts_dir, f"run_crew_{crew.name.lower().replace(' ', '_')}_{int(time.time())}.py")
            
            # Load agent and task configurations
            with open("config/agents.yaml", "r") as f:
                agents_config = yaml.safe_load(f)
            
            with open("config/tasks.yaml", "r") as f:
                tasks_config = yaml.safe_load(f)
            
            # Generate script content
            script_content = self.generate_script_content(crew, agents_config, tasks_config)
            
            # Write script to file
            with open(script_path, "w") as f:
                f.write(script_content)
            
            return script_path
        
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to generate script: {str(e)}")
            return None
    
    def generate_script_content(self, crew, agents_config, tasks_config):
        """Generate the content of the Python script"""
        script = [
            "#!/usr/bin/env python",
            "from crewai import Agent, Task, Crew, Process",
            "",
            "def main():",
            "    # Nota: Las herramientas específicas se han desactivado temporalmente",
            "    # debido a problemas de compatibilidad",
            "    tools = {}",
            "",
            "    # Create agents",
        ]
        
        # Add agents
        for agent_name in crew.agents:
            if agent_name in agents_config:
                agent_data = agents_config[agent_name]
                agent_tools = agent_data.get("tools", [])
                tools_str = ", ".join([f"tools['{tool}']" for tool in agent_tools if tool])
                
                script.append(f"    {agent_name.lower().replace(' ', '_')}_agent = Agent(")
                script.append(f"        role=\"{agent_data.get('role', '')}\",")
                script.append(f"        goal=\"{agent_data.get('goal', '')}\",")
                script.append(f"        backstory=\"{agent_data.get('backstory', '')}\",")
                script.append(f"        verbose={str(agent_data.get('verbose', True)).lower()},")
                script.append(f"        allow_delegation={str(agent_data.get('allow_delegation', False)).lower()},")
                if tools_str:
                    script.append(f"        tools=[{tools_str}]")
                script.append("    )")
                script.append("")
        
        script.append("    # Create tasks")
        
        # Add tasks
        for task_name in crew.tasks:
            if task_name in tasks_config:
                task_data = tasks_config[task_name]
                agent_name = task_data.get("agent", "")
                if agent_name in crew.agents:
                    script.append(f"    {task_name.lower().replace(' ', '_')}_task = Task(")
                    script.append(f"        description=\"{task_data.get('description', '')}\",")
                    script.append(f"        expected_output=\"{task_data.get('expected_output', '')}\",")
                    script.append(f"        agent={agent_name.lower().replace(' ', '_')}_agent,")
                    output_file = task_data.get("output_file", "")
                    if output_file:
                        script.append(f"        output_file=\"{output_file}\"")
                    script.append("    )")
                    script.append("")
        
        # Create crew
        script.append("    # Create crew")
        script.append("    crew = Crew(")
        script.append("        agents=[" + ", ".join([f"{agent.lower().replace(' ', '_')}_agent" for agent in crew.agents]) + "],")
        script.append("        tasks=[" + ", ".join([f"{task.lower().replace(' ', '_')}_task" for task in crew.tasks]) + "],")
        script.append(f"        process=Process.{crew.process},")
        script.append(f"        verbose={str(crew.verbose).lower()}")
        script.append("    )")
        script.append("")
        script.append("    # Run the crew")
        script.append("    result = crew.kickoff()")
        script.append("    print(\"\\nCrew execution completed!\")")
        script.append("    print(\"Result:\", result)")
        script.append("    return result")
        script.append("")
        script.append("if __name__ == \"__main__\":")
        script.append("    main()")
        
        return "\n".join(script)

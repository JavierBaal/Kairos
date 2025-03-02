from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QTextEdit, QPushButton, QListWidget, QFormLayout, 
    QComboBox, QMessageBox, QInputDialog, QFileDialog
)
from PyQt6.QtCore import Qt
import yaml
import os
import sys

# Add the parent directory to sys.path to make the models module accessible
sys.path.append('/Users/vanguardhive/Desktop/TRABAJOS/SALA-CREATIVA/CrewalAIGui')
from models.task_model import TaskModel

class TaskPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.tasks = {}
        self.init_ui()
        
    def init_ui(self):
        layout = QHBoxLayout(self)
        
        # Left panel - Task list
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        
        self.task_list = QListWidget()
        self.task_list.itemClicked.connect(self.load_task)
        
        left_layout.addWidget(QLabel("Tasks:"))
        left_layout.addWidget(self.task_list)
        
        button_layout = QHBoxLayout()
        self.add_button = QPushButton("Add Task")
        self.delete_button = QPushButton("Delete Task")
        self.add_button.clicked.connect(self.add_task)
        self.delete_button.clicked.connect(self.delete_task)
        
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.delete_button)
        left_layout.addLayout(button_layout)
        
        # Right panel - Task details
        right_panel = QWidget()
        self.right_layout = QFormLayout(right_panel)
        
        self.task_name = QLineEdit()
        self.task_description = QTextEdit()
        self.task_expected_output = QTextEdit()
        self.task_agent = QComboBox()
        self.task_output_file = QLineEdit()
        self.browse_button = QPushButton("Browse...")
        self.browse_button.clicked.connect(self.browse_output_file)
        
        output_file_layout = QHBoxLayout()
        output_file_layout.addWidget(self.task_output_file)
        output_file_layout.addWidget(self.browse_button)
        
        self.right_layout.addRow("Name:", self.task_name)
        self.right_layout.addRow("Description:", self.task_description)
        self.right_layout.addRow("Expected Output:", self.task_expected_output)
        self.right_layout.addRow("Agent:", self.task_agent)
        self.right_layout.addRow("Output File:", output_file_layout)
        
        # Save button
        self.save_task_button = QPushButton("Save Task")
        self.save_task_button.clicked.connect(self.save_current_task)
        self.right_layout.addRow(self.save_task_button)
        
        # Add panels to main layout
        layout.addWidget(left_panel, 1)
        layout.addWidget(right_panel, 2)
        
        # Load existing tasks
        self.load_tasks()
        
    def add_task(self):
        name, ok = QInputDialog.getText(self, "Add Task", "Task Name:")
        if ok and name:
            if name in self.tasks:
                QMessageBox.warning(self, "Warning", "Task with this name already exists")
                return
                
            self.tasks[name] = TaskModel(name=name)
            self.task_list.addItem(name)
            self.clear_form()
            self.task_name.setText(name)
    
    def delete_task(self):
        current_item = self.task_list.currentItem()
        if current_item:
            name = current_item.text()
            confirm = QMessageBox.question(
                self, "Confirm Deletion", 
                f"Are you sure you want to delete task '{name}'?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if confirm == QMessageBox.StandardButton.Yes:
                self.tasks.pop(name, None)
                self.task_list.takeItem(self.task_list.row(current_item))
                self.clear_form()
    
    def load_task(self, item):
        name = item.text()
        if name in self.tasks:
            task = self.tasks[name]
            self.task_name.setText(task.name)
            self.task_description.setText(task.description)
            self.task_expected_output.setText(task.expected_output)
            
            # Set agent if available
            if task.agent:
                index = self.task_agent.findText(task.agent)
                if index >= 0:
                    self.task_agent.setCurrentIndex(index)
            
            self.task_output_file.setText(task.output_file)
    
    def save_current_task(self):
        name = self.task_name.text()
        if not name:
            QMessageBox.warning(self, "Warning", "Task name cannot be empty")
            return
            
        task = TaskModel(
            name=name,
            description=self.task_description.toPlainText(),
            expected_output=self.task_expected_output.toPlainText(),
            agent=self.task_agent.currentText(),
            output_file=self.task_output_file.text()
        )
        
        # Update or add task
        self.tasks[name] = task
        
        # Update list if it's a new task
        found = False
        for i in range(self.task_list.count()):
            if self.task_list.item(i).text() == name:
                found = True
                break
        
        if not found:
            self.task_list.addItem(name)
            
        QMessageBox.information(self, "Success", f"Task '{name}' saved successfully")
    
    def clear_form(self):
        self.task_name.clear()
        self.task_description.clear()
        self.task_expected_output.clear()
        self.task_agent.setCurrentIndex(0)
        self.task_output_file.clear()
    
    def browse_output_file(self):
        file_name, _ = QFileDialog.getSaveFileName(
            self, "Select Output File", "", "All Files (*)"
        )
        if file_name:
            self.task_output_file.setText(file_name)
    
    def save_tasks(self):
        # Convert tasks to YAML format
        tasks_dict = {}
        for name, task in self.tasks.items():
            tasks_dict[name] = {
                "description": task.description,
                "expected_output": task.expected_output,
                "agent": task.agent,
                "output_file": task.output_file
            }
        
        # Ensure config directory exists
        os.makedirs("config", exist_ok=True)
        
        # Save to YAML file
        with open("config/tasks.yaml", "w") as f:
            yaml.dump(tasks_dict, f)
    
    def load_tasks(self):
        try:
            if os.path.exists("config/tasks.yaml"):
                with open("config/tasks.yaml", "r") as f:
                    tasks_dict = yaml.safe_load(f)
                
                if tasks_dict:
                    self.tasks = {}
                    self.task_list.clear()
                    
                    for name, data in tasks_dict.items():
                        task = TaskModel(
                            name=name,
                            description=data.get("description", ""),
                            expected_output=data.get("expected_output", ""),
                            agent=data.get("agent", ""),
                            output_file=data.get("output_file", "")
                        )
                        
                        self.tasks[name] = task
                        self.task_list.addItem(name)
        except Exception as e:
            QMessageBox.warning(self, "Warning", f"Failed to load tasks: {str(e)}")
    
    def get_tasks(self):
        return self.tasks
        
    def update_agents(self, agents):
        """Update the agent dropdown with available agents"""
        current_agent = self.task_agent.currentText()
        self.task_agent.clear()
        
        # Add empty option
        self.task_agent.addItem("")
        
        # Add all agents
        for agent_name in agents.keys():
            self.task_agent.addItem(agent_name)
        
        # Restore selection if possible
        if current_agent:
            index = self.task_agent.findText(current_agent)
            if index >= 0:
                self.task_agent.setCurrentIndex(index)
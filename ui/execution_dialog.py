from PyQt6.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QPushButton, QHBoxLayout
from PyQt6.QtCore import QProcess, Qt, pyqtSignal

class ExecutionDialog(QDialog):
    execution_finished = pyqtSignal(bool)  # Signal to indicate execution finished (success/failure)
    
    def __init__(self, title="Crew Execution"):
        super().__init__()
        self.setWindowTitle(title)
        self.resize(800, 600)
        self.process = None
        
        # Create layout
        layout = QVBoxLayout(self)
        
        # Output text area
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
        self.output_text.setStyleSheet("font-family: monospace; background-color: #1e1e1e; color: #f0f0f0;")
        layout.addWidget(self.output_text)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.close_button = QPushButton("Close")
        self.close_button.clicked.connect(self.close)
        self.stop_button = QPushButton("Stop Execution")
        self.stop_button.clicked.connect(self.stop_execution)
        
        button_layout.addWidget(self.stop_button)
        button_layout.addWidget(self.close_button)
        layout.addLayout(button_layout)
    
    def execute_script(self, script_path):
        """Execute the generated script and show output in real-time"""
        self.process = QProcess()
        self.process.readyReadStandardOutput.connect(self.handle_stdout)
        self.process.readyReadStandardError.connect(self.handle_stderr)
        self.process.finished.connect(self.handle_finished)
        
        self.output_text.clear()
        self.output_text.append(f"Executing script: {script_path}\n")
        self.output_text.append("=" * 80 + "\n")
        
        # Start the process
        self.process.start("python", [script_path])
    
    def handle_stdout(self):
        """Handle standard output from the process"""
        data = self.process.readAllStandardOutput().data().decode()
        self.output_text.append(data)
        # Scroll to bottom
        cursor = self.output_text.textCursor()
        cursor.movePosition(cursor.MoveOperation.End)
        self.output_text.setTextCursor(cursor)
    
    def handle_stderr(self):
        """Handle standard error from the process"""
        data = self.process.readAllStandardError().data().decode()
        self.output_text.append(f"<span style='color:red;'>{data}</span>")
        # Scroll to bottom
        cursor = self.output_text.textCursor()
        cursor.movePosition(cursor.MoveOperation.End)
        self.output_text.setTextCursor(cursor)
    
    def handle_finished(self, exit_code, exit_status):
        """Handle process completion"""
        if exit_code == 0:
            self.output_text.append("\n" + "=" * 80)
            self.output_text.append("\nExecution completed successfully!")
            self.execution_finished.emit(True)
        else:
            self.output_text.append("\n" + "=" * 80)
            self.output_text.append(f"\nExecution failed with exit code: {exit_code}")
            self.execution_finished.emit(False)
        
        self.stop_button.setEnabled(False)
    
    def stop_execution(self):
        """Stop the running process"""
        if self.process and self.process.state() == QProcess.ProcessState.Running:
            self.process.terminate()
            self.process.waitForFinished(3000)  # Wait up to 3 seconds
            if self.process.state() == QProcess.ProcessState.Running:
                self.process.kill()  # Force kill if not terminated
            
            self.output_text.append("\n" + "=" * 80)
            self.output_text.append("\nExecution stopped by user.")
            self.stop_button.setEnabled(False)
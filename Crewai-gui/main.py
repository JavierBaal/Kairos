import sys
from PyQt6.QtWidgets import QApplication
from ui.task_panel import TaskPanel

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TaskPanel()
    window.show()
    sys.exit(app.exec())
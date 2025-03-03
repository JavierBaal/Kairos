from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt, pyqtProperty

class StepProgress(QWidget):
    def __init__(self, steps, current_step=0, parent=None):
        super().__init__(parent)
        self.steps = steps
        self.current_step = current_step
        self._setup_ui()
        
    def _setup_ui(self):
        layout = QHBoxLayout()
        layout.setSpacing(16)  # Espaciado entre pasos
        self.setLayout(layout)
        
        self.step_indicators = []
        
        for i, step in enumerate(self.steps):
            # Crear indicador de paso
            indicator = self._create_step_indicator(i + 1, step)
            self.step_indicators.append(indicator)
            layout.addWidget(indicator)
            
            # Añadir conector si no es el último paso
            if i < len(self.steps) - 1:
                connector = self._create_connector()
                layout.addWidget(connector)
        
        self._update_states()
    
    def _create_step_indicator(self, number, label_text):
        container = QWidget()
        container.setProperty("step-container", True)
        
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        container.setLayout(layout)
        
        # Círculo con número
        circle = QLabel(str(number))
        circle.setFixedSize(48, 48)
        circle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        circle.setProperty("step-indicator", True)
        layout.addWidget(circle)
        
        # Texto del paso
        label = QLabel(label_text)
        label.setProperty("step-label", True)
        layout.addWidget(label)
        
        return container
    
    def _create_connector(self):
        connector = QWidget()
        connector.setFixedWidth(32)
        connector.setProperty("step-connector", True)
        return connector
    
    def _update_states(self):
        for i, indicator in enumerate(self.step_indicators):
            circle = indicator.findChild(QLabel)
            
            # Limpiar estados anteriores
            circle.setProperty("active", False)
            circle.setProperty("completed", False)
            
            # Establecer estado actual
            if i < self.current_step:
                circle.setProperty("completed", True)
                circle.setText("✓")  # Marca de verificación
            elif i == self.current_step:
                circle.setProperty("active", True)
            
            # Forzar actualización de estilos
            circle.style().unpolish(circle)
            circle.style().polish(circle)
    
    @pyqtProperty(int)
    def currentStep(self):
        return self.current_step
    
    @currentStep.setter
    def currentStep(self, step):
        if 0 <= step <= len(self.steps):
            self.current_step = step
            self._update_states()
    
    def next_step(self):
        """Avanza al siguiente paso si es posible."""
        if self.current_step < len(self.steps):
            self.currentStep = self.current_step + 1
    
    def previous_step(self):
        """Retrocede al paso anterior si es posible."""
        if self.current_step > 0:
            self.currentStep = self.current_step - 1
    
    def reset(self):
        """Reinicia el progreso al primer paso."""
        self.currentStep = 0

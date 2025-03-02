#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script para ejecutar Kairos con la interfaz simplificada.
Este script carga el panel de flujo de trabajo simplificado en lugar del original.
"""

import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QStatusBar
from PyQt6.QtCore import Qt

# Añadir el directorio raíz al path para importaciones
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importar componentes de Kairos
from ui.workflow_panel_simplified import WorkflowPanelSimplified
from ui.theme import Theme

class MainWindow(QMainWindow):
    """Ventana principal de Kairos con interfaz simplificada"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kairos - Inteligencia Competitiva")
        self.setMinimumSize(1200, 800)
        
        # Configurar tema
        self.init_theme()
        
        # Configurar UI
        self.init_ui()
        
    def init_theme(self):
        """Inicializar tema visual"""
        # Aplicar paleta de colores
        self.setPalette(Theme.get_palette("mixed"))
        
    def init_ui(self):
        """Inicializar interfaz de usuario"""
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # Título de la aplicación
        title_label = QLabel("KAIROS INTELLIGENCE SYSTEM")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: white;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Subtítulo
        subtitle_label = QLabel("Plataforma de Inteligencia Competitiva")
        subtitle_label.setStyleSheet("font-size: 16px; color: #d0d0d8;")
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Panel de flujo de trabajo simplificado
        self.workflow_panel = WorkflowPanelSimplified()
        
        # Añadir componentes al layout principal
        main_layout.addWidget(title_label)
        main_layout.addWidget(subtitle_label)
        main_layout.addWidget(self.workflow_panel, 1)  # 1 = stretch factor
        
        # Barra de estado
        status_bar = QStatusBar()
        status_bar.showMessage("Listo")
        self.setStatusBar(status_bar)

def main():
    """Función principal para ejecutar la aplicación"""
    app = QApplication(sys.argv)
    
    # Aplicar hoja de estilos global
    app.setStyleSheet(Theme.get_stylesheet("mixed"))
    
    # Crear y mostrar ventana principal
    window = MainWindow()
    window.show()
    
    # Ejecutar bucle de eventos
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

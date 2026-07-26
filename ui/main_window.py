from PyQt6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Converter")
        self.setMinimumSize(700,500)
        
        label = QLabel("Перетащите файлы сюда")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont()
        font.setPointSize(18)
        label.setFont(font)

         
         
        layout = QVBoxLayout()
        layout.addWidget(label)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
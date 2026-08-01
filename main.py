import sys
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow
from pathlib import Path
import converters

def main():
    app = QApplication(sys.argv)
    style_path = Path(__file__).parent/"resources"/"styles"/"dark.qss"
    if style_path.exists():
        app.setStyleSheet(style_path.read_text(encoding="utf-8"))
        
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
    
if __name__ == "__main__":
    main()
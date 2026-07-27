from pathlib import Path

from PyQt6.QtWidgets import (
    QMainWindow, QLabel, QVBoxLayout, QWidget,
    QPushButton, QFileDialog, QMessageBox, QComboBox,
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

from core.registry import find_converter, get_all
from core.task import ConvertTask


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Converter")
        self.setMinimumSize(700, 500)
        self.setAcceptDrops(True)

        self.current_file: Path | None = None

        title = QLabel("Перетащи файлы сюда")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont()
        font.setPointSize(18)
        title.setFont(font)

        self.file_label = QLabel("Файл не выбран")
        self.file_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.format_combo = QComboBox()
        self._update_formats()

        btn_select = QPushButton("Выбрать файл")
        btn_select.clicked.connect(self.select_file)

        btn_convert = QPushButton("Конвертировать")
        btn_convert.clicked.connect(self.convert_file)

        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addWidget(self.file_label)
        layout.addWidget(self.format_combo)
        layout.addWidget(btn_select)
        layout.addWidget(btn_convert)
        layout.addWidget(self.status_label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
    
    def _update_formats(self):
        self.format_combo.clear()
        all_formats = set()
        for converter in get_all():
            all_formats.update(converter.supported_output())  
        for fmt in sorted(all_formats):
            self.format_combo.addItem(fmt)    

    def select_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите файл",
            "",
            "Изображения (*.png *.jpg *.jpeg *.bmp *.tiff *.webp *.gif);;Все файлы (*)",
        )
        if path:
            self.current_file = Path(path)
            self.file_label.setText(f"Файл: {self.current_file.name}")
            self.status_label.setText("")

    def convert_file(self):
        if not self.current_file:
            QMessageBox.warning(self, "Ошибка", "Сначала выбери файл!")
            return
        output_format = self.format_combo.currentText() 
        output_path = self.current_file.with_suffix(output_format)

        if output_path == self.current_file:
            self.status_label.setText(f"Файл уже в формате {output_format}")
            return

        task = ConvertTask(self.current_file, output_path)
        if not task.resolve_converter():
            QMessageBox.warning(self, "Ошибка", f"нет конвертора для {self.current_file.suffix}")
            return

        try:
            task.execute()
            self.status_label.setText(f"Готово! Сохранено: {output_path.name}")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
    def dropEvent(self, event):
        urls=event.mimeData().urls()
        if urls:
            path = Path(urls[0].toLocalFile())
            self.current_file = path
            self.file_label.setText(f"Файл: {path.name}")
            self.status_label.setText("")                
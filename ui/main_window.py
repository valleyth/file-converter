from pathlib import Path

from PyQt6.QtWidgets import (
    QMainWindow, QLabel, QVBoxLayout, QWidget,
    QPushButton, QFileDialog, QMessageBox,
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

from core.registry import find_converter
from core.task import ConvertTask


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Converter")
        self.setMinimumSize(700, 500)

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

        btn_select = QPushButton("Выбрать файл")
        btn_select.clicked.connect(self.select_file)

        btn_convert = QPushButton("Конвертировать в PNG")
        btn_convert.clicked.connect(self.convert_file)

        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addWidget(self.file_label)
        layout.addWidget(btn_select)
        layout.addWidget(btn_convert)
        layout.addWidget(self.status_label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

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

        output_path = self.current_file.with_suffix(".png")

        if output_path == self.current_file:
            self.status_label.setText("Файл уже в формате PNG")
            return

        task = ConvertTask(self.current_file, output_path)
        if not task.resolve_converter():
            QMessageBox.warning(self, "Ошибка", "Конвертер не найден!")
            return

        try:
            task.execute()
            self.status_label.setText(f"Готово! Сохранено: {output_path.name}")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))
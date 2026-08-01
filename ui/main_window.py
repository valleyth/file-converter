from pathlib import Path

from PyQt6.QtWidgets import (
    QMainWindow, QLabel, QVBoxLayout, QWidget,
    QPushButton, QFileDialog, QMessageBox, QComboBox,
)
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtCore import Qt

from core.registry import find_converter, get_all, get_supported_outputs
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

        self.preview_label = QLabel("")
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

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
        layout.addWidget(self.preview_label)
        layout.addWidget(self.format_combo)
        layout.addWidget(btn_select)
        layout.addWidget(btn_convert)
        layout.addWidget(self.status_label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
    
    def _update_formats(self):
        self.format_combo.clear()
        if not self.current_file:
            return
        input_ext = self.current_file.suffix.lower()
        formats = get_supported_outputs(input_ext) 
        for fmt in formats:
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
            self.show_preview(self.current_file)
            self._update_formats()
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
            self.show_preview(self.current_file)
            self._update_formats()
            self.status_label.setText("")                
    def show_preview (self, path:Path)->None:
        if path.suffix.lower() in [".png", ".jpg", ".jpeg", ".bmp", ".webp", ".tiff", ".gif"]:
            pixmap = QPixmap(str(path))
            scaled = pixmap.scaled(
                200, 100,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            ) 
            self.preview_label.setPixmap(scaled)
        else:
            self.preview_label.clear()           
from pathlib import Path

from PyQt6.QtWidgets import (
    QMainWindow, QLabel, QVBoxLayout, QWidget,
    QPushButton, QFileDialog, QMessageBox, QComboBox,
    QListWidget, QProgressBar,
)
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtCore import Qt

from core.registry import get_supported_outputs
from core.task import ConvertTask
from core.worker import ConvertWorker


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Converter")
        self.setMinimumSize(700, 500)
        self.setAcceptDrops(True)

        self.files: list[Path] = []
        self.worker: ConvertWorker | None = None

        title = QLabel("Перетащи файлы сюда")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont()
        font.setPointSize(18)
        title.setFont(font)

        self.file_list = QListWidget()
        self.preview_label = QLabel("")
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.format_combo = QComboBox()

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 1)
        self.progress_bar.setValue(0)

        btn_select = QPushButton("Выбрать файлы")
        btn_select.clicked.connect(self.select_files)

        self.btn_convert = QPushButton("Конвертировать")
        self.btn_convert.clicked.connect(self.convert_files)

        self.btn_cancel = QPushButton("Отмена")
        self.btn_cancel.setEnabled(False)
        self.btn_cancel.clicked.connect(self.cancel_conversion)
        
        self.btn_remove = QPushButton("Удалить выбранный файл")
        self.btn_remove.clicked.connect(self.remove_selected)

        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addWidget(self.file_list)
        layout.addWidget(self.preview_label)
        layout.addWidget(self.format_combo)
        layout.addWidget(self.progress_bar)
        layout.addWidget(btn_select)
        layout.addWidget(self.btn_convert)
        layout.addWidget(self.btn_cancel)
        layout.addWidget(self.btn_remove)
        layout.addWidget(self.status_label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def select_files(self):
        paths, _ = QFileDialog.getOpenFileNames(
            self,
            "Выберите файлы",
            "",
            "Все файлы (*)",
        )
        if paths:
            self.files = [Path(p) for p in paths]
            self._update_file_list()
            self.show_preview(self.files[0])
            self._update_formats()
            self.status_label.setText("")

    def _update_file_list(self):
        self.file_list.clear()
        for f in self.files:
            self.file_list.addItem(f.name)

    def _update_formats(self):
        self.format_combo.clear()
        if not self.files:
            return
        all_formats = set()
        for f in self.files:
            all_formats.update(get_supported_outputs(f.suffix.lower()))
        for fmt in sorted(all_formats):
            self.format_combo.addItem(fmt)

    def convert_files(self):
        if not self.files:
            QMessageBox.warning(self, "Ошибка", "Сначала выбери файлы!")
            return

        output_format = self.format_combo.currentText()
        if not output_format:
            QMessageBox.warning(self, "Ошибка", "Нет доступных форматов для выбранных файлов!")
            return

        tasks = []
        skipped = []
        for input_path in self.files:
            output_path = input_path.with_suffix(output_format)
            if output_path == input_path:
                skipped.append(f"{input_path.name} (уже {output_format})")
                continue
            task = ConvertTask(input_path, output_path)
            if not task.resolve_converter():
                skipped.append(f"{input_path.name} (нет конвертера {input_path.suffix} → {output_format})")
                continue
            tasks.append(task)

        self._skipped = skipped

        if not tasks:
            if skipped:
                self.status_label.setText("Ничего не конвертировано: " + ", ".join(skipped))
            else:
                self.status_label.setText("Все файлы уже в целевом формате")
            return

        self.worker = ConvertWorker(tasks)
        self.worker.progressChanged.connect(self._on_progress)
        self.worker.conversionFinished.connect(self._on_finished)
        self.worker.taskFailed.connect(self._on_task_failed)
        self.worker.start()

        self.status_label.setText("Конвертация запущена...")
        self.btn_convert.setEnabled(False)
        self.btn_cancel.setEnabled(True)
    def cancel_conversion(self):
        if self.worker:
            self.worker.cancel()
            self.status_label.setText("Отмена...")    

    def _on_progress(self, current, total, name):
        self.progress_bar.setMaximum(total)
        self.progress_bar.setValue(current + 1)
        self.status_label.setStyleSheet("color: #64b5f6;")
        self.status_label.setText(f"[{current + 1}/{total}] {name}")

    def _on_finished(self, success, fail):
        self.progress_bar.setValue(0)
        self.btn_convert.setEnabled(True)
        self.btn_cancel.setEnabled(False)
        msg = f"Готово! Успешно: {success}, ошибок: {fail}"
        if getattr(self, "_skipped", None):
            msg += " Пропущено: " + ", ".join(self._skipped)
        if fail > 0:
            self.status_label.setStyleSheet("color: #ef5350;")
        else:
            self.status_label.setStyleSheet("color: #66bb6a;")
        self.status_label.setText(msg)

    def _on_task_failed(self, message):
        self.status_label.setStyleSheet("color: #ef5350;")
        self.status_label.setText(f"Ошибка: {message}")

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            self.file_list.setStyleSheet(
                "QListWidget { border: 2px solid #1e88e5; background-color: #3c3c3c; border-radius: 5px; }"
            )
            event.acceptProposedAction()

    def dragLeaveEvent(self, event):
        self.file_list.setStyleSheet("")
        event.accept()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        paths = [Path(u.toLocalFile()) for u in urls if u.isLocalFile()]
        if paths:
            for p  in paths:
                if p not in self.files:
                    self.files.append(p)
            self._update_file_list()
            self.show_preview(self.files[0])
            self._update_formats()
            self.status_label.setText("")

    def show_preview(self, path: Path) -> None:
        if path.suffix.lower() in [".png", ".jpg", ".jpeg", ".bmp", ".webp", ".tiff", ".gif"]:
            pixmap = QPixmap(str(path))
            scaled = pixmap.scaled(
                400, 300,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            self.preview_label.setPixmap(scaled)
        else:
            self.preview_label.clear()     
    def remove_selected (self):
        row = self.file_list.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Ошибка", "Выберите файл в списке!")    
            return
        del self.files[row]
        self.file_list.takeItem(row)
        if self.files:
            self.show_preview(self.files[0])
        else:
            self.preview_label.clear()
        self._update_formats()                
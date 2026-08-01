from PyQt6.QtCore import QThread, pyqtSignal

from core.task import ConvertTask


class ConvertWorker(QThread):
    progressChanged = pyqtSignal(int, int, str)
    conversionFinished = pyqtSignal(int, int)
    taskFailed = pyqtSignal(str)

    def __init__(self, tasks: list[ConvertTask]):
        super().__init__()
        self.tasks = tasks
        self._cancelled = False

    def run(self) -> None:
        total = len(self.tasks)
        success = 0
        fail = 0
        for i, task in enumerate(self.tasks):
            if self._cancelled:
                break
            self.progressChanged.emit(i, total, task.input_path.name)
            try:
                task.execute()
                success += 1
            except Exception as e:
                fail += 1
                self.taskFailed.emit(f"{task.input_path.name}: {e}")
        self.conversionFinished.emit(success, fail)

    def cancel(self) -> None:
        self._cancelled = True
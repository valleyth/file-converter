from pathlib import Path
from enum import Enum

from core.converter import BaseConverter
from core.registry import find_converter

class TaskStatus(Enum):
    PENDING="pending"
    RUNNING="running"
    DONE="done"
    FAILED="failed"
    
    class ConvertTask: 
        def __init__(self, input_path: Path, output_path: Path, options: dict | None = None):
            self.input_path = input_path
            self.output_path = output_path
            self.options = options or {}
            self.status = TaskStatus.PENDING
            self.error: str | None = None
            self.converter: BaseConverter | None = None
            
            
        def resolve_converter (self) -> bool:
            input_ext = self.input_path.suffix.lower()
            output_ext = self.output_path.suffix.lower()
            self.converter = find_converter(input_ext, output_ext)
            
            def execute(self) -> None:
                if not self.converter:
                    raise RuntimeError("Конвертор не найден. Сначала Вызови resolve_converter()")
                self.status = TaskStatus.RUNNING
                try:
                    self.converter.convert(self.input_path, self.output_path, self.options)
                    self.status = TaskStatus.DONE
                except Exception as e:
                    self.status = TaskStatus.FAILED
                    self.error = str(e)       
            
    
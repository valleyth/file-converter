from abc import ABC, abstractmethod
from pathlib import Path

class BaseConverter(ABC):
    
    @abstractmethod
    def supported_input(self)-> list[str]:
        pass
    
    @abstractmethod
    def supported_output(self)->list[str]:
        pass
    
    @abstractmethod
    def convert(self, input_path: Path, output_path: Path, options: dict) -> None:
        pass
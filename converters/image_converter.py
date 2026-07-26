from pathlib import Path
from PIL import Image
from core.converter import BaseConverter

class ImageConverter (BaseConverter):
    def supported_input(self) -> list[str]:
        return [".png", ".jpg", ".jpeg", ".bmp", ".webp", ".tiff", ".gif"]
    def supported_output(self) -> list[str]:
        return [".png", ".jpg", ".jpeg", ".bmp", ".webp", ".tiff"]
    def convert(self, input_path: Path, output_path:Path, options: dict)->None:
        img=Image.open(input_path)
        img.save(output_path)
        
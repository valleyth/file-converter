from pathlib import Path
from PIL import image
from core.converter import BaseConverter

class ImageConverter (BaseConverter):
    def supported_input(self) -> list[str]:
        return [".png", ".jpg", ".jpeg", ".bmp", ".webp", ".tiff", ".gif"]
    def supported_output(self) -> list[str]:
        return [".png", ".jpg", ".jpeg", ".bmp", ".webp", ".tiff"]
    def convert(Path, input_path: Path, output_path:Path, options: dict)->None:
        img=image.open(input_path)
        img.save(output_path)
        
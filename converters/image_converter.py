from pathlib import Path
import rawpy
from PIL import Image
from core.converter import BaseConverter
RAW_EXTENSIONS = [".cr2", ".cr3", ".nef", ".arw", ".srf", ".dng", ".orf", ".raf", ".rw2"]
class ImageConverter (BaseConverter):
    def supported_input(self) -> list[str]:
        return [".png", ".jpg", ".jpeg", ".bmp", ".webp", ".tiff", ".gif"] + RAW_EXTENSIONS
    def supported_output(self) -> list[str]:
        return [".png", ".jpg", ".jpeg", ".bmp", ".webp", ".tiff"]
    def convert(self, input_path: Path, output_path:Path, options: dict)->None:
        input_ext = input_path.suffix.lower()
        if input_ext in RAW_EXTENSIONS:
            with rawpy.imread(str(input_path)) as raw:
                rgb = raw.postprocess()
            img = Image.fromarray(rgb)
        else:
            img = Image.open(input_path)
                  
        img.save(output_path)
        
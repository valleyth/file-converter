from pathlib import Path
import fitz
from core.converter import BaseConverter

class DocumentConverter(BaseConverter):
    def supported_input(self) -> list[str]:
        return [".pdf", ".txt"]
    def supported_output(self) -> list[str]:
        return [".pdf", ".txt"]
    def convert(self, input_path:Path, output_path:Path, options:dict)->None:
        input_ext = input_path.suffix.lower()
        output_ext = output_path.suffix.lower()
        if input_ext == ".pdf" and output_ext == ".txt":
            self._pdf_to_txt(input_path, output_path)
        elif input_ext == ".txt" and output_ext == ".pdf":
             self._txt_to_pdf(input_path, output_path)
        else:
            raise ValueError(f"Неподдержиемая конвертация: {input_ext} -> {output_ext}")         
    def _pdf_to_txt(self, input_path:Path, output_path:Path) -> None:
        doc=fitz.open(str(input_path))
        text=""
        for page in doc:
            text+=page.get_text() or ""
        doc.close()    
        output_path.write_text(text, encoding="utf-8")
    def _txt_to_pdf(self, input_path: Path, output_path: Path)->None:
        from fpdf import FPDF
        text = input_path.read_text(encoding="utf-8")         
        pdf=FPDF()
        pdf.add_page()
        pdf.set_font("Helvetica", size=12)
        pdf.multi_cell(0, 10, text)
        pdf.output(str(output_path))   
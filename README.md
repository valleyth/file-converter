# File Converter

Конвертер файлов с графическим интерфейсом на Python + PyQt6.

Поддерживает конвертацию изображений, документов и RAW форматов.

## Возможности

- Конвертация изображений (PNG, JPG, BMP, WebP, TIFF, GIF)
- Поддержка RAW форматов (CR2, NEF, ARW, DNG, ORF, RAF)
- Конвертация документов (PDF, TXT, DOCX)
- Пакетная конвертация нескольких файлов
- Drag & drop
- Превью изображений
- Прогресс и отмена конвертации
- Тёмная тема

## Установка

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Запуск

```bash
python3 main.py
```

## Конвертеры

| Формат | Библиотека |
|--------|-----------|
| Изображения | Pillow, rawpy |
| PDF | PyMuPDF, pdf2docx |
| DOCX | python-docx |
| PDF из TXT | fpdf2 |

## Сборка в exe

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name file-converter main.py
```

## Зависимости

Для конвертации DOCX → PDF требуется LibreOffice (Linux) или Microsoft Word (Windows).

## Лицензия

MIT License — подробнее: [MIT](https://opensource.org/licenses/MIT)

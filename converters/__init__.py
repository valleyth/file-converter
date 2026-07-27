from core.registry import register
from converters.image_converter import ImageConverter
from converters.document_converter import DocumentConverter

register(ImageConverter())
register(DocumentConverter())
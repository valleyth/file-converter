from core.converter import BaseConverter


_converters: list[BaseConverter] = []


def register(converter: BaseConverter) -> None:
    _converters.append(converter)


def get_all() -> list[BaseConverter]:
    return _converters.copy()


def find_converter(input_ext: str, output_ext: str) -> BaseConverter | None:
    for converter in _converters:
        if input_ext in converter.supported_input() and output_ext in converter.supported_output():
            return converter
    return None
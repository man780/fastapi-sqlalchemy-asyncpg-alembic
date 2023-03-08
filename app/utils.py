import logging
from functools import lru_cache

from rich.console import Console
from rich.logging import RichHandler

console = Console(color_system="256", width=200, style="blue")


@lru_cache
def get_logger(module_name):
    logger = logging.getLogger(module_name)
    handler = RichHandler(
        rich_tracebacks=True, console=console, tracebacks_show_locals=True
    )
    handler.setFormatter(
        logging.Formatter("[ %(threadName)s:%(funcName)s:%(lineno)d ] - %(message)s")
    )
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    return logger


def get_data_by_xml_element(element_name: str, **kwargs):
    """Get XML element and take text from this"""
    if "is_int" in kwargs:
        value: int = 0
        if element_name:
            value = element_name.text or 0
        return value
    if "is_str" in kwargs:
        value: str = ""
        if element_name:
            value = element_name.text or ""
        return value

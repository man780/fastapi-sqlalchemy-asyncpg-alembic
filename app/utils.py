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

def filter_cars(cls, stmt, payload):
    for key, value in payload:
        if key == "page" or key == "limit":
            continue
        if key == "make" and value != "":
            _attr = getattr(cls, key)
            stmt = stmt.where(_attr == value)
        if key == "model" and value != "":
            _attr = getattr(cls, key)
            stmt = stmt.where(_attr == value)
        if key == "year" and value != 0:
            _attr = getattr(cls, key)
            stmt = stmt.where(_attr == value)
        
        if key == "price" and value != 0:
            _attr = getattr(cls, key)
            if value == 1:
                stmt = stmt.where(_attr <= 3000)
            elif value == 2:
                stmt = stmt.where(_attr > 3000, _attr <= 4000)
            elif value == 3:
                stmt = stmt.where(_attr > 4000, _attr <= 5000)
            elif value == 4:
                stmt = stmt.where(_attr > 5000, _attr <= 10000)
            elif value == 5:
                stmt = stmt.where(_attr > 10000, _attr <= 50000)
            elif value == 6:
                stmt = stmt.where(_attr > 50000, _attr <= 100000)
            else:
                stmt = stmt.where(_attr > 100000)
        
        if key == "mileage" and value != 0:
            _attr = getattr(cls, key)
            if value == 1:
                stmt = stmt.where(_attr <= 0)
            elif value == 2:
                stmt = stmt.where(_attr > 0, _attr <= 5000)
            elif value == 3:
                stmt = stmt.where(_attr > 5000, _attr <= 10000)
            elif value == 4:
                stmt = stmt.where(_attr > 10000, _attr <= 20000)
            elif value == 5:
                stmt = stmt.where(_attr > 20000, _attr <= 30000)
            elif value == 6:
                stmt = stmt.where(_attr > 30000, _attr <= 40000)
            elif value == 7:
                stmt = stmt.where(_attr > 40000, _attr <= 50000)
            elif value == 8:
                stmt = stmt.where(_attr > 50000, _attr <= 60000)
            elif value == 9:
                stmt = stmt.where(_attr > 70000, _attr <= 80000)
            elif value == 10:
                stmt = stmt.where(_attr > 90000, _attr <= 100000)
            else:
                stmt = stmt.where(_attr > 100000)
    return stmt

import pandas as pd
import random

def hex_to_rgb(hex: str) -> tuple[int, int, int]:
    hex = hex.lstrip('#')
    return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))

def instrument_sans(font_weight: str) -> str:
    return f"assets/fonts/ttf/InstrumentSans-{font_weight}.ttf"

def to_file(text: str):
    return str(text).replace(" ", "-").lower()

def format_data(column, dataframe: pd.DataFrame) -> list:
    if isinstance(column, str):
        return dataframe[column]
    elif isinstance(column, pd.Series) or isinstance(column, list):
        return column
    else:
        raise TypeError("Column must be a string or a pandas Series")

def random_id(a: int = 1000, b: int = 9999) -> int:
    return random.randint(a, b)
from fpdf import FPDF
import pandas as pd

def hex_to_rgb(hex: str):
    hex = hex.lstrip('#')
    return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))

def file(text: str):
    return str(text).replace(" ", "-").lower()

def string_or_series(column, dataframe: pd.DataFrame):
    if isinstance(column, str):
        return dataframe[column]
    elif isinstance(column, pd.Series):
        return column
    else:
        raise TypeError("Column must be a string or a pandas Series")
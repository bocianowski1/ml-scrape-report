# PDF library
from enum import Enum
from fpdf import FPDF
import time

# Visualization libraries
import pandas as pd
import plotly.express as px

# Custom libraries
from utils.helpers import *
from utils.constants import *
from utils.errors import PlotError, InputError

class PDF(FPDF):
    def __init__(self, title, **kwargs):
        super(PDF, self).__init__(**kwargs)
        # Setting parameters
        self.title = title

        # Adding custom fonts
        self.add_font(DEFAULT_FONT, "", instrument_sans("Regular"), uni=True)
        self.add_font(DEFAULT_FONT, "b", instrument_sans("Bold"), uni=True)
        self.add_font(DEFAULT_FONT, "i", instrument_sans("Italic"), uni=True)

        # Setting fonts
        r, g, b = hex_to_rgb(colors_dict["Primary Dark"])
        self.set_text_color(r, g, b)
        self.set_font(DEFAULT_FONT, '', DEFAULT_FONT_SIZE)

        # Setting layout
        self.set_margins(MARGIN, MARGIN-5, MARGIN)
        self.set_auto_page_break(True, MARGIN)
        self.add_page()

    # Overriding header and footer
    def header(self):
        self.set_font(DEFAULT_FONT, '', TITLE_FONT_SIZE)
        r, g, b = hex_to_rgb(colors_dict["Header Dark"])
        self.set_text_color(r, g, b)
        self.cell(0, 10, self.title, 0, 0, 'L')
        self.ln(8)
    
        self.set_font(DEFAULT_FONT, '', DEFAULT_FONT_SIZE)
        r, g, b = hex_to_rgb(colors_dict["Header Dark"])
        self.set_text_color(r, g, b)
        today = time.strftime("%d/%m/%Y")
        self.cell(0, 10, str(today), 0, 0, 'L')
        self.ln(8)

    def footer(self):
        self.set_y(-15)
        self.set_font(DEFAULT_FONT, 'I', DEFAULT_FONT_SIZE)
        r, g, b = hex_to_rgb(colors_dict["Secondary Dark"])
        self.set_text_color(r, g, b)
        self.cell(0, 10, str(self.page_no()), 0, 0, 'C')

class ChartType(Enum):
    LINE = 1
    PIE = 2
    BAR = 3

def visualization_preprocesser(data: pd.DataFrame, title: str, parent_directory: str, x_column: str, y_column: str) -> tuple[str, str, list, list]:
    image_filename = to_file(title)
    parent_directory = parent_directory if parent_directory[-1] == "/" else parent_directory + "/"
    x = format_data(data[x_column], data)
    y = format_data(data[y_column], data)
    return image_filename, parent_directory, x, y

def save_image(pdf: PDF, fig, image_filename: str, parent_directory: str, image_format: str, width: int = None) -> None:
    try:
        fig.write_image(f"{parent_directory}{image_filename}.{image_format}")
        pdf.image(f"{parent_directory}{image_filename}.{image_format}", w=pdf.epw if width is None else width)
    except PlotError:
        return
    
def visualize(pdf: PDF, chart_type: ChartType, data: pd.DataFrame, x_column: str, y_column: str, title: str,
              width: int = None, parent_directory: str = "assets/images/", image_format: str = "svg", colors: list[str] = None) -> None:
    
    image_filename, parent_directory, x, y = visualization_preprocesser(data, title, parent_directory, x_column, y_column)
    if chart_type == ChartType.LINE:
        fig = px.line(data, x=x, y=y, color=SECONDARY_BLUE)
    elif chart_type == ChartType.PIE:
        if colors is None:
            colors = px.colors.sequential.RdBu
        fig = px.pie(data, values=x, names=y, title=title, color_discrete_sequence=colors)
    elif chart_type == ChartType.BAR:
        fig = px.bar(data, x=x, y=y, color=SECONDARY_BLUE)
    else:
        raise InputError("Invalid chart type.")
    fig.update_layout(plot_bgcolor="white")
    save_image(pdf, fig, image_filename, parent_directory, image_format, width)


def add_table(pdf: PDF, data: pd.DataFrame, width: int = 160, col_width = (80, 40, 40)) -> None:
    try:
        data = data.applymap(str)

        columns = [list(data)]
        rows = data.values.tolist()
        data = columns + rows
    except InputError:
        return

    with pdf.table(borders_layout="MINIMAL",
        cell_fill_color=200,
        cell_fill_mode="ROWS",
        line_height=DEFAULT_FONT_SIZE * 2.5,
        text_align="CENTER",
        width=width, col_width=col_width) as table:

        for data_row in data:
            row = table.row()
            for datum in data_row:
                row.cell(datum)
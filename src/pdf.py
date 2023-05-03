from fpdf import FPDF
import time

from utils.helpers import *
from utils.constants import *
from utils.visualize import *

class PlotType:
    LINE = "line"
    PIE = "pie"

class PDF(FPDF):
    def __init__(self, title, **kwargs):
        super(PDF, self).__init__(**kwargs)
        # Setting parameters
        self.title = title

        # Adding custom fonts
        self.add_font(DEFAULT_FONT, "", "assets/fonts/ttf/InstrumentSans-Regular.ttf", uni=True)
        self.add_font(DEFAULT_FONT, "b", "assets/fonts/ttf/InstrumentSans-Bold.ttf", uni=True)
        self.add_font(DEFAULT_FONT, "i", "assets/fonts/ttf/InstrumentSans-Italic.ttf", uni=True)

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
        large_break(self)
    
        self.set_font(DEFAULT_FONT, '', DEFAULT_FONT_SIZE)
        r, g, b = hex_to_rgb(colors_dict["Header Dark"])
        self.set_text_color(r, g, b)
        today = time.strftime("%d/%m/%Y")
        self.cell(0, 10, str(today), 0, 0, 'L')
        large_break(self)

    def footer(self):
        self.set_y(-15)
        self.set_font(DEFAULT_FONT, 'I', DEFAULT_FONT_SIZE)
        r, g, b = hex_to_rgb(colors_dict["Secondary Dark"])
        self.set_text_color(r, g, b)
        self.cell(0, 10, str(self.page_no()), 0, 0, 'C')

def add_plot(pdf: PDF, plot_function, data: pd.DataFrame, title: str, x_column: str, y_column: str, xlabel: str = None, ylabel: str = None, padding: tuple[int, int] = (0, 0), width: int = 80):
    try:
        plot_function(data, x_column, y_column, title, xlabel, ylabel, show_plot=False)

        px, py = padding[0], padding[1]
        pdf.image(f"../assets/images/plot.png", x=pdf.l_margin + px, y=MARGIN + py, w=width)
    except:
        return


def columns(pdf: PDF, y: int, contents: list[str]):
    n_cols = len(contents)
    col_width = int(WIDTH / n_cols)
    for i in range(n_cols):
        if ".png" in contents[i]:
            try:
                pdf.image(f"../assets/images/{contents[i]}", 
                          x=(i * col_width), y=y, w=col_width-MARGIN)
            except:
                continue
        else:
            pdf.cell(col_width-MARGIN, y, contents[i], 1)
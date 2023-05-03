# from openbb import *
import pandas as pd

from pdf import PDF, add_plot, columns
from utils.visualize import create_piechart

def main() -> None:
    pdf = PDF(title="Pelagi Daily Report")
    columns(pdf, 200, ["Content", "Content"])
    pdf.output("pelagi-report.pdf", "F")

if __name__ == "__main__":
    main()
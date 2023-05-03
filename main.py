# from openbb import *
import pandas as pd

from pdf import PDF, add_plot, columns
from src.utils.visualize import create_piechart

def main() -> None:
    pdf = PDF(title="Pelagi Daily Report")
    pdf.output("pelagi-report.pdf", "F")

if __name__ == "__main__":
    main()
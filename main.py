# from openbb import *
import pandas as pd
from pdf import PDF, ChartType, visualize
from dotenv import load_dotenv


def main() -> None:
    pdf = PDF(title="Pelagi Daily Report")
    
    pdf.output("pelagi-report.pdf")

if __name__ == "__main__":
    main()
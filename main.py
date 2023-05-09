# from openbb import *
import pandas as pd
from pdf import PDF, ChartType, visualize, add_dataframe
from data.sentiment_analysis import get_sentiment, analyze_dataframe


def main() -> None:
    pdf = PDF(title="Pelagi Daily Report")
    data = pd.read_csv("data/sentiment-6729.csv")

    add_dataframe(pdf, data[["Description", "Sentiment", "Confidence"]])
    
    pdf.output("pelagi-report.pdf")

if __name__ == "__main__":
    main()
from dotenv import load_dotenv
import pandas as pd
import asyncio
import time

# from report.pdf import PDF
from data.scraping.scrape import scrape
from data.scraping.utils.helpers import print_results
from data.ml.sentiment_analysis import analyze_dataframe, load_model

# def make_report():
#     pdf = PDF(title="Pelagi Report")
#     pdf.output("pelagi-report.pdf")



def main() -> None:
    start_time = time.time()
    load_dotenv()
    print("Starting...")
    model_params = load_model()

    # news_df = pd.read_csv("data/results/news_earnings.csv")
    # print(news_df.head())

    loop = asyncio.get_event_loop()
    loop.run_until_complete(scrape(test=True, model_params=model_params))
    # data = loop.run_until_complete(scrape(test=True))

    elapsed_time = time.time() - start_time
    print(f"\nElapsed time: {elapsed_time}")


if __name__ == "__main__":
    main()
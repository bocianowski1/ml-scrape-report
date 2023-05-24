from dotenv import load_dotenv
import pandas as pd
import asyncio
import time

# from report.pdf import PDF
from data.scraping.scrape import scrape
# from data.ml.sentiment_analysis import analyze_dataframe, load_model

def make_report():
    # pdf = PDF(title="Pelagi Daily Report")
    # pdf.output("pelagi-report.pdf")
    pass


def main() -> None:
    start_time = time.time()
    load_dotenv()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(scrape(test=True))

    elapsed_time = time.time() - start_time
    print(f"Elapsed time: {elapsed_time}")


if __name__ == "__main__":
    main()
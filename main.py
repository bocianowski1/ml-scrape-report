from dotenv import load_dotenv
import asyncio
import time

# from report.pdf import PDF
from data.scraping.scrape import scrape
from data.database.db import drop_table
from data.ml.sentiment_analysis import load_model

# def make_report():
#     pdf = PDF(title="Pelagi Report")
#     pdf.output("pelagi-report.pdf")


def main() -> None:
    start_time = time.time()
    drop_table("news")
    load_dotenv()
    print("Starting...")
    model_params = load_model()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(scrape(test=True, model_params=model_params))
    # data = loop.run_until_complete(scrape(test=True))

    elapsed_time = time.time() - start_time
    print(f"\nElapsed time: {elapsed_time}")


if __name__ == "__main__":
    main()
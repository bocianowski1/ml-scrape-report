import asyncio
import aiohttp
from bs4 import BeautifulSoup
import time

from .utils.helpers import soupify, clean_value, get_sites, get_proxies, random_index
from .utils.helpers import print_progress, print_results
from .browser.selenium_browser import parse
from ..ml.sentiment_analysis import get_sentiment
from ..database.db import write_to_db


CONNECTOR_LIMIT = 50
ABSOLUTE_PATH = "/Users/torgerbocianowski/Desktop/Projects/pelagi/"
DATA_PATH = ABSOLUTE_PATH + "data/"
SCRAPING_PATH = DATA_PATH + "scraping/"
RESULTS_PATH = DATA_PATH + "results/"


async def get_table_data(session: aiohttp.ClientSession, url: str, db_name: str, parse_info: dict = None, proxy: str = None) -> list[dict]:
    async with session:
        if parse_info["scroll"] or parse_info["load"]:
            url = await parse(url, **parse_info)
            soup = BeautifulSoup(url, "html.parser")
        else:
            soup = await soupify(session, url, proxy)
            if not soup:
                raise Exception("Could not soupify")

        table = soup.find("table")
        if not table:
            print("table not found")
            return []
        headers = [header.text for header in table.find_all("th")]
        if len(headers) == 0:
            headers = [header.text for header in table.find_all("td")]
        table_rows = table.find_all("tr")[1:]
        if not table_rows:
            print("table rows not found")
            return []

        data = []
        for row in table_rows:
            item = {}
            for i, cell in enumerate(row.find_all("td")):
                val = cell.text
                try:
                    val = clean_value(val)
                except:
                    pass
                item[headers[i]] = val
            data.append(item)
            # write_to_db(db_name, tuple(item.values()))
        # if filename:
        #     write_csv(headers, data, filename)
        return data

async def get_list_data(session: aiohttp.ClientSession, url: str, db_name: str, parse_info: dict = None, proxy: str = None,
                        html_info: dict = None, model_params: tuple = None):
    async with session:
        if parse_info["scroll"] or parse_info["load"]:
            url = await parse(url, **parse_info, popup=html_info["popup"])
            soup = BeautifulSoup(url, "html.parser")
        else:
            soup = await soupify(session, url, proxy)
            if not soup:
                raise Exception("Could not soupify")
        container_tag, list_tag, header_tag, description_tag, attrs = html_info["container_tag"], html_info["list_tag"], \
                                                                html_info["header_tag"], html_info["description_tag"], \
                                                                html_info["attrs"]
        if container_tag:
            list_ = soup.find(container_tag, attrs={"id": attrs["id"]}).find(list_tag)
        else:
            list_ = soup.find(list_tag)
        if not list_:
            return
        list_items = list_.find_all("li")

        # data = []
        for item in list_items:
            headline = item.find(header_tag).text
            description = item.find(description_tag).text
            if headline and description:
                # data.append(NewsArticle(headline=headline, description=description))
                text = headline + "\n\n" + description
                sentiment, confidence = get_sentiment(text, *model_params)
                write_to_db(db_name, (headline, description, sentiment, str(confidence)))
            else:
                continue
        # return data

async def scrape_site(session: aiohttp.ClientSession, proxy: str, site: dict, 
                      topic: str, subtopic: str, result: list[dict], model_params: tuple = None) -> None:
    base_url = site["base_url"]
    current = site["topics"][topic][subtopic]
    url = base_url + current["url"]
    parse_info = current["parse_info"]
    db_name = current["db_name"]
    if current["structure"]["table"]:
        print(f"scraping {url}")
        try:
            data = await get_table_data(session, url, db_name, parse_info=parse_info, proxy=proxy)
            result.append(data)
            print_progress(data)
        except Exception as e:
            print(f"\nERROR @ scrape_site() [table]\nurl: {url}")
            print(e)
    elif current["structure"]["list"]:
        print(f"scraping {url}")
        html_info = current["html_info"]
        try:
            data = await get_list_data(session, url, db_name, parse_info=parse_info, proxy=proxy, 
                                       html_info=html_info, model_params=model_params)
            result.append(data)
            # print_progress(data)
        except Exception as e:
            print(f"\nERROR @ scrape_site() [list]\nurl: {url}")
            print(e)
    else:
        print(f"not table or list {url}")

async def scrape(test=False, model_params: tuple = None) -> list[dict]:
    proxies = get_proxies()
    sites = get_sites(test=test)

    result = []
    tasks = []
    n = len(proxies)
    connector = aiohttp.TCPConnector(limit=CONNECTOR_LIMIT)
    async with aiohttp.ClientSession(connector=connector) as session:
        for site in sites:
            topics = sites[site]["topics"]
            for topic in topics:
                subtopics = topics[topic]
                for subtopic in subtopics:
                    proxy = proxies[random_index(n)]
                    task = scrape_site(session, proxy, sites[site], topic, subtopic, result, model_params)
                    tasks.append(task)
                    await asyncio.sleep(0.1)
        await asyncio.gather(*tasks)
    return result


# if __name__ == "__main__":
#     start_time = time.time()

#     loop = asyncio.get_event_loop()
#     data = loop.run_until_complete(scrape())

#     elapsed_time = time.time() - start_time
#     print_results(data)
#     print(f"Elapsed time: {elapsed_time}")
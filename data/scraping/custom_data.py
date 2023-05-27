import aiohttp
from bs4 import BeautifulSoup

from .browser.selenium_browser import parse
from scraping.scrape import soupify


async def get_custom_data(session: aiohttp.ClientSession, url: str, custom: dict, parse_info: dict = None, proxy: str = None) -> list[dict]:
    async with session:
        if parse_info["scroll"] or parse_info["load"]:
            url = await parse(url, **parse_info, sleep=3.0)
            soup = BeautifulSoup(url, "html.parser")
        else:
            soup = await soupify(session, url, proxy)
            if not soup:
                raise Exception("Could not soupify")
            
        if custom["type"]["table"]:
            table = custom["type"]["table"]
            body = table["body"]
            header = body["header"]
            rows = body["rows"]

            result = soup.find(body["tag"], attrs={"role": body["role"], "class": body["class"]})
            # header_html = body_html.find(header["tag"], attrs={"role": header["role"], "class": header["class"]})
            # rows_html = body_html.find_all(rows["tag"], attrs={"role": rows["role"], "class": rows["class"]})
            print(result, "result")
        data = []
        return data
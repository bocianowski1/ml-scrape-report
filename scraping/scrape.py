import asyncio
import json
import aiohttp
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

CONNECTOR_LIMIT = 50

def get_sites() -> dict:
    return json.loads(open("sites.json").read())

async def soupify(session: aiohttp.ClientSession, url: str, proxy: str = None) -> BeautifulSoup:
    try:
        async with session.get(url, proxy=proxy) as response:
            if response.status != 200:
                print(f"\nERROR @ soupify()\nstatus code: {response.status}")
                return None
            content = await response.text()
            return BeautifulSoup(content, "html.parser")
    except Exception as e:
        print(f"\nERROR @ soupify()")
        print(e)
        return None


def set_options():
    options = Options()
    options.headless = True
    options.set_preference("dom.disable_beforeunload", True)
    options.set_preference("intl.accept_languages", "en-US")
    return options


async def parse(url: str, sleep: float = 1.0, popup: dict = None, scroll: bool = False,
                load: bool = False) -> str:
    print(f"enter parse()\nurl: {url}")
    if not scroll and not load:
        return url
    
    options = set_options()
    try:
        response = webdriver.Firefox(options=options)
        response.get(url)
        if scroll:
            scroll_down(response, popup=popup)
        elif load:
            print("loading...")
            await asyncio.sleep(sleep)
        html = response.page_source
        response.quit()
        return html
    except Exception as e:
        print(f"\nERROR @ parse()\nurl: {url}")
        print(e)
        return url


def scroll_down(driver: webdriver.Firefox, sleep: float = 0.75, popup: dict = None, num_iters: int = 5) -> None:
    print("enter scroll_down()")
    if popup:
        try:
            if popup["scroll_button"]:
                driver.find_element_by_id(popup["scroll_button"]).click()
            driver.find_element_by_name(popup["reject"]).click()
        except Exception as e:
            print(f"\nERROR @ scroll_down()\n{e}")
            return None

    print("scrolling...")
    for i in range(num_iters):
        print(f"{i+1}/{num_iters}", end=" ")
        html = driver.find_element(By.TAG_NAME, 'html')
        html.send_keys(Keys.END)
        time.sleep(sleep)
    print()


async def get_table_data(session: aiohttp.ClientSession, url: str, parse_info: dict = None, proxy: str = None) -> list[dict]:
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
            return []
        headers = [header.text for header in table.find_all("th")]
        if len(headers) == 0:
            headers = [header.text for header in table.find_all("td")]
        table_rows = table.find_all("tr")[1:]
        if not table_rows:
            return []
        print("headers", headers)

        data = []
        for row in table_rows:
            item = {}
            for i, cell in enumerate(row.find_all("td")):
                item[headers[i]] = cell.text
            data.append(item)
        return data


async def get_list_data(session: aiohttp.ClientSession, url: str, parse_info: dict = None, proxy: str = None,
                        html_info: dict = None) -> list[dict]:
    async with session:
        if parse_info["scroll"] or parse_info["load"]:
            url = await parse(url, **parse_info, popup=html_info["popup"])
            soup = BeautifulSoup(url, "html.parser")
        else:
            soup = await soupify(session, url, proxy)
            if not soup:
                raise Exception("Could not soupify")
        container_tag, list_tag, header_tag, description_tag = html_info["container_tag"], html_info["list_tag"], \
                                                               html_info["header_tag"], html_info["description_tag"]
        attrs = html_info["attrs"]
        if container_tag:
            list_ = soup.find(container_tag, attrs={"id": attrs["id"]}).find(list_tag)
        else:
            list_ = soup.find(list_tag)
        if not list_:
            return []
        list_items = list_.find_all("li")

        data = []
        for item in list_items:
            headline = item.find(header_tag).text
            description = item.find(description_tag).text
            if headline and description:
                data.append({
                    "headline": headline,
                    "description": description,
                })
        return data


def get_proxies() -> list[str]:
    with open("proxies.txt") as f:
        return f.read().splitlines()


async def scrape_site(session: aiohttp.ClientSession, proxy: str, site: dict, topic: str, subtopic: str, result: list[dict]):
    base_url = site["base_url"]
    current = site["topics"][topic][subtopic]
    url = base_url + current["url"]
    if current["structure"]["table"]:
        url = base_url + current["url"]
        print(f"scraping {url}")
        parse_info = current["parse_info"]
        try:
            data = await get_table_data(session, url, parse_info=parse_info, proxy=proxy)
            result.append(data)
            print("-" * 100)
            print(data, len(data))
            print("-" * 100)
        except Exception as e:
            print(f"\nERROR @ scrape() [table]\nurl: {url}")
            print(e)
    elif current["structure"]["list"]:
        url = base_url + current["url"]
        print(f"scraping {url}")
        parse_info = current["parse_info"]
        html_info = current["html_info"]
        try:
            data = await get_list_data(session, url, parse_info=parse_info, proxy=proxy, html_info=html_info)
            result.append({
                "topic": topic,
                "subtopic": subtopic,
                "data": data
            })
            print("-" * 100)
            print(data, len(data))
            print("-" * 100)
        except Exception as e:
            print(f"\nERROR @ scrape() [list]\nurl: {url}")
            print(e)
    else:
        print(f"not table or list {url}")


async def scrape() -> list[dict]:
    proxies = get_proxies()
    sites = get_sites()

    result = []
    tasks = []
    connector = aiohttp.TCPConnector(limit=CONNECTOR_LIMIT)
    async with aiohttp.ClientSession(connector=connector) as session:
        for site in sites:
            print(site)
            topics = sites[site]["topics"]
            for topic in topics:
                subtopics = topics[topic]
                for subtopic in subtopics:
                    proxy = proxies.pop(0)
                    task = scrape_site(session, proxy, sites[site], topic, subtopic, result)
                    tasks.append(task)
                    if not proxies:
                        proxies = get_proxies()
                    await asyncio.sleep(0.1)
        await asyncio.gather(*tasks)
    return result


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    data = loop.run_until_complete(scrape())
    for news in data:
        print(news)
        print()
    print(len(data))

import time
import json
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

# SCRAPING
def get_sites() -> dict:
    return json.loads(open("sites.json").read())

def soupify(url: str, proxy: str = None) -> BeautifulSoup:
    try:
        r = requests.get(url, proxies={"http": proxy, "https": proxy})
        if r.status_code != 200:
            print(f"error @ soupify()\nstatus code: {r.status_code}")
            return None
        return BeautifulSoup(r.text, "html.parser")
    except Exception as e:
        print(f"error @ soupify()")
        print(e)
        return None
    
def set_options():
    options = Options()
    options.headless = True
    options.set_preference("dom.disable_beforeunload", True)
    options.set_preference("intl.accept_languages", "en-US")
    return options

def parse(url: str, sleep: float = 1.0, popup: dict = None, scroll: bool = False, load: bool = False) -> str:
    print(f"enter parse()\nurl: {url}")
    if not scroll and not load: 
        return url
    options = set_options()
    try:
        response = webdriver.Firefox(options=options)
        response.get(url)
        if scroll:
            print("enter scroll_down()")
            scroll_down(response, popup=popup)
        elif load:
            print("loading...")
            time.sleep(sleep)
        html = response.page_source
        response.quit()
        return html
    except Exception as e:
        print(f"error @ parse()\nurl: {url}")
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
            print(f"error @ scroll_down()\n{e}")
            return None

    print("scrolling...")
    for i in range(num_iters):
        print(f"{i}/{num_iters}", end=" ")
        html = driver.find_element(By.TAG_NAME, 'html')
        html.send_keys(Keys.END)
        time.sleep(sleep)
    print()


def get_table_data(url: str, parse_info: dict = None, proxy: str = None) -> list[dict]:
    if parse_info["scroll"] or parse_info["load"]:
        url = parse(url, **parse_info)
        soup = BeautifulSoup(url, "html.parser")
    else:
        soup = soupify(url, proxy)
        if not soup:
            raise Exception("Could not soupify")
        
    table = soup.find("table")
    if table is None:
        return []
    headers = [header.text for header in table.find_all("th")]
    table_rows = table.find_all("tr")[1:]
    if not table_rows:
        print("no table rows")
        return []

    data = []
    for row in table_rows:
        item = {}
        for i, cell in enumerate(row.find_all("td")):
            item[headers[i]] = cell.text
        data.append(item)
    return data

def get_list_data(url: str, parse_info: dict = None, proxy: str = None, html_info: dict = None) -> list[dict]:
    if parse_info["scroll"] or parse_info["load"]:
        url = parse(url, **parse_info, popup=html_info["popup"])
        soup = BeautifulSoup(url, "html.parser")
    else:
        soup = soupify(url, proxy)
        if not soup:
            raise Exception("Could not soupify")
    container_tag, list_tag, header_tag, description_tag = html_info["container_tag"], html_info["list_tag"], html_info["header_tag"], html_info["description_tag"]
    attrs = html_info["attrs"]
    if container_tag:
        list_ = soup.find(container_tag, attrs={"id": attrs["id"]}).find(list_tag)
    else:
        list_ = soup.find(list_tag)
    if list_ is None:
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
    
# PROXIES
def get_proxies() -> list[str]:
    with open("proxies.txt") as f:
        return f.read().splitlines()
    
def scrape() -> list[dict]:
    proxies = get_proxies()
    sites = get_sites()

    result = []
    counter = 0
    for site in sites:
        if site != "global_rates":
            continue
        base_url = sites[site]["base_url"]
        topics = sites[site]["topics"]
        for topic in topics:
            subtopics = topics[topic]
            for subtopic in subtopics:
                current = subtopics[subtopic]
                print(current)
                if current["structure"]["table"]:
                    url = base_url + current["url"]
                    print(f"scraping {url}")
                    parse_info = current["parse_info"]
                    try:
                        data = get_table_data(url,
                                             parse_info=parse_info,
                                             proxy=proxies[counter])
                        result.append(data)
                    except Exception as e:
                        print(f"error @ scrape() [table]\nurl: {url}")
                        print(e)
                        continue
                elif current["structure"]["list"]:
                    url = base_url + current["url"]
                    print(f"scraping {url}")
                    parse_info = current["parse_info"]
                    html_info = current["html_info"]
                    try:
                        data = get_list_data(url,
                                             parse_info=parse_info,
                                             proxy=proxies[counter],
                                             html_info=html_info)
                        result.append({
                            "topic": topic,
                            "subtopic": subtopic,
                            "data": data
                        })
                    except Exception as e:
                        print(f"error @ scrape() [list]\nurl: {url}")
                        print(e)
                        continue
                else:
                    print(f"not table or list {url}")
                    continue

                counter += 1
                if counter == len(proxies):
                    counter = 0

    return result

if __name__ == "__main__":
    data = scrape()
    for news in data:
        print(news)
        print()
    print(len(data))
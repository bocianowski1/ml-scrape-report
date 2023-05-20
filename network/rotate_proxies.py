import json
import requests
from bs4 import BeautifulSoup

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


def get_table_data(url: str, proxy: str = None, attrs: dict = None) -> list[dict]:
    soup = soupify(url, proxy)
    if not soup:
        raise Exception("Could not soupify")
    table = soup.find("table", attrs)
    if table is None:
        return []
    headers = [header.text for header in table.find_all("th")]
    table_rows = table.find_all("tr")[1:]

    data = []
    for row in table_rows:
        item = {}
        for i, cell in enumerate(row.find_all("td")):
            item[headers[i]] = cell.text
        data.append(item)
    return data

def get_list_data(url: str, proxy: str = None, container_tag: str = None, attrs: dict = None,
                  list_tag: str = "ul", headline_tag: str = "h3", desc_tag: str = "p") -> list[dict]:
    soup = soupify(url, proxy)
    if not soup:
        raise Exception("Could not soupify")
    if container_tag:
        list_ = soup.find(container_tag, attrs={"id": attrs["id"]}).find(list_tag)
    else:
        list_ = soup.find(list_tag)
    if list_ is None:
        return []
    list_items = list_.find_all("li")

    data = []
    for item in list_items:
        headline = item.find(headline_tag).text
        description = item.find(desc_tag).text
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
    
def scrape():
    proxies = get_proxies()
    sites = get_sites()

    result = []
    counter = 0
    for site in sites:
        if site != "cme":
            continue
        base_url = sites[site]["base_url"]
        topics = sites[site]["topics"]
        for topic in topics:
            subtopics = topics[topic]
            for subtopic in subtopics:
                current = subtopics[subtopic]
                if current["table"]:
                    url = base_url + current["url"]
                    try:
                        data = get_table_data(url,
                                              proxy=proxies[counter],
                                              attrs=current["attrs"])
                        result.append(data)
                    except Exception as e:
                        print(f"error @ scrape() [table]\nurl: {url}")
                        print(e)
                        continue
                elif current["list"]:
                    try:
                        container_tag = current["container_tag"]
                    except:
                        container_tag = None
                    url = base_url + current["url"]
                    try:
                        data = get_list_data(url,
                                            proxy=proxies[counter],
                                            container_tag=container_tag, 
                                            attrs=current["attrs"])
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
    print(data)
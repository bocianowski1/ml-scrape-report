import csv
import json
import aiohttp
from bs4 import BeautifulSoup
import random


ABSOLUTE_PATH = "/Users/torgerbocianowski/Desktop/Projects/pelagi/"
DATA_PATH = ABSOLUTE_PATH + "data/"
SCRAPING_PATH = DATA_PATH + "scraping/"
RESULTS_PATH = DATA_PATH + "results/"

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

def clean_value(value: str) -> str:
    value = value.strip()
    if value == '-':
        return None
    try:
        return float(value.replace(",", ""))
    except ValueError:
        return value
    
def random_index(length: int) -> int:
    return random.randint(0, length - 1)
    
def get_sites(test=False) -> dict:
    json_file = "test.sites.json" if test else "sites.json"
    json_file = SCRAPING_PATH + json_file
    return json.loads(open(json_file).read())

def write_csv(headers: list, data: list, filename: str) -> None:
    if not filename.endswith(".csv"):
        filename = filename + ".csv"
    if not filename.startswith("/"):
        filename = "/" + filename
    with open(RESULTS_PATH + filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)

def get_proxies(filename: str = "proxies.txt") -> list[str]:
    proxy_list_file = SCRAPING_PATH + filename
    with open(proxy_list_file) as f:
        return f.read().splitlines()

def print_progress(data: list[dict]) -> None:
    print("-" * 100, f"\nData: {data}\nLength: {len(data)}\n", "-" * 100)

def print_results(data: list[dict]) -> None:
    for item in data:
        print(item, len(item), "\n")
    print(f"Length: {len(data)}")
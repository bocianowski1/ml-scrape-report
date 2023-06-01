import csv
import json
import random
import re

ABSOLUTE_PATH = "/Users/torgerbocianowski/Desktop/Projects/pelagi/"
DATA_PATH = ABSOLUTE_PATH + "data/"
SCRAPING_PATH = DATA_PATH + "scraping/"
RESULTS_PATH = DATA_PATH + "results/"

def clean_value(value: str) -> str:
    if isinstance(value, bool) or isinstance(value, tuple):
        return str(value)
    if isinstance(value, float) or isinstance(value, int):
        return value
    if isinstance(value, str):
        value = value.lower().strip()
        if value == '-' or value == "n/a" or value == "nan" or value == "none" or value == "" or value == " ":
            return "NULL"
        if value.startswith("$") or value.startswith("€") or value.startswith("£") or value.startswith("+") or value.startswith("-"):
            value = value[1:]
        if value.endswith("%"):
            value = value[:-1]
    try:
        return float(value.replace(",", ""))
    except ValueError:
        return value

def clean_data(data: tuple) -> tuple:
    return tuple([clean_value(value) for value in data])

def clean_column_name(name: str) -> str:
    if name.startswith("%"):
        name = "perc_" + name[1:]
    cleaned_string = re.sub(r'[^a-zA-Z0-9 ]', '', name).strip()
    if cleaned_string.startswith("52"):
        cleaned_string = "fifty_two" + cleaned_string[2:]
    return cleaned_string.replace(' ', '_').lower()

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
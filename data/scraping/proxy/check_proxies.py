import threading
from queue import Queue
import requests

ABSOLUTE_PATH = "/Users/torgerbocianowski/Desktop/Projects/pelagi/"
DATA_PATH = ABSOLUTE_PATH + "data/"
SCRAPING_PATH = DATA_PATH + "scraping/"
PROXY_PATH = SCRAPING_PATH + "proxy/"

q = Queue()
# test_url = "http://ipinfo.io/json"
test_url = "https://finance.yahoo.com/topic/earnings"

with open(PROXY_PATH + "proxies_all.txt") as f:
    proxies = f.read().splitlines()
    for proxy in proxies:
        q.put(proxy)

def check_proxies():
    global q
    while not q.empty():
        proxy = q.get()
        try:
            r = requests.get(test_url, proxies={"http": proxy, "https": proxy})
        except:
            continue
        if r.status_code == 200:
            with open(SCRAPING_PATH + "proxies.txt", "a") as f:
                f.write(proxy + "\n")


for _ in range(10):
    threading.Thread(target=check_proxies).start()
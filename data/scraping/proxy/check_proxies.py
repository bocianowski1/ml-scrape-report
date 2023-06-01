import asyncio
import aiohttp
import os

ABSOLUTE_PATH = os.path.dirname(os.path.abspath(__file__)) + "/"
SCRAPING_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/"
PROXY_PATH = SCRAPING_PATH + "proxy/"

test_url = "https://finance.yahoo.com/topic/earnings"

async def check_proxies(proxy_queue):
    async with aiohttp.ClientSession() as session:
        while not proxy_queue.empty():
            proxy = proxy_queue.get()
            try:
                async with session.get(test_url, proxy=proxy) as response:
                    if response.status == 200:
                        with open(SCRAPING_PATH + "proxies.txt", "a") as f:
                            f.write(proxy + "\n")
            except aiohttp.ClientError:
                continue

async def main():
    proxy_queue = asyncio.Queue()

    with open(PROXY_PATH + "proxies_all.txt") as f:
        proxies = f.read().splitlines()
        for proxy in proxies:
            await proxy_queue.put(proxy)

    tasks = []
    for _ in range(10):
        task = asyncio.create_task(check_proxies(proxy_queue))
        tasks.append(task)

    await asyncio.gather(*tasks)

# if __name__ == "__main__":
#     asyncio.run(main())

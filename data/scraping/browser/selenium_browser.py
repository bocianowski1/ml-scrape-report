import asyncio
import time
from selenium import webdriver
from bs4 import BeautifulSoup
import aiohttp
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

def set_options(headless = True) -> Options:
    options = Options()
    options.headless = headless
    options.set_preference("dom.disable_beforeunload", True)
    options.set_preference("intl.accept_languages", "en-US")
    return options

async def soupify(session: aiohttp.ClientSession, url: str, proxy: str = None) -> BeautifulSoup:
    try:
        async with session.get(url, proxy=proxy) as response:
            if response.status != 200:
                print(f"\nERROR @ soupify()\nstatus code: {response.status}")
                return None
            html = await response.text()
            return BeautifulSoup(html, "html.parser")
    except Exception as e:
        print(f"\nERROR @ soupify()")
        print(e)
        return None
    
def get_popup(html_info: dict, parse_info: dict):
    try:
        popup = html_info["popup"] if html_info else None
        if popup:
            parse_info["load"] = True
        return popup
    except:
        return None

def remove_popup(driver: webdriver.Firefox, popup: dict) -> None:
    try:
        if popup["scroll_button"]:
            driver.find_element(By.ID, popup["scroll_button"]).click()
            driver.find_element(By.NAME, popup["reject"]).click()
    except Exception as e:
        print(f"\nERROR @ remove_popup()\n{e}")
        return None

async def parse(url: str, sleep: float = 1.0, popup: dict = None, scroll: bool = False,
                load: bool = False) -> str:
    if popup:
        load = True
    if not scroll and not load:
        return url
    try:
        driver = webdriver.Firefox(options=set_options())
        driver.get(url)
        if popup:
            remove_popup(driver, popup)
        if scroll:
            scroll_down(driver)
        elif load:
            print("loading...")
            await asyncio.sleep(sleep)
        html = driver.page_source
        driver.quit()
        return html
    except Exception as e:
        print(f"\nERROR @ parse()\nurl: {url}")
        raise e

def scroll_down(driver: webdriver.Firefox, sleep: float = 0.5, num_iters: int = 5) -> None:
    print("scrolling...")
    for _ in range(num_iters):
        html = driver.find_element(By.TAG_NAME, 'html')
        html.send_keys(Keys.END)
        time.sleep(sleep)

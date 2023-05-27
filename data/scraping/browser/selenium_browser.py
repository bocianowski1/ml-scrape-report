import asyncio
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

def set_options() -> Options:
    options = Options()
    options.headless = True
    options.set_preference("dom.disable_beforeunload", True)
    options.set_preference("intl.accept_languages", "en-US")
    return options

async def parse(url: str, sleep: float = 1.0, popup: dict = None, scroll: bool = False,
                load: bool = False) -> str:
    if not scroll and not load:
        return url
    try:
        response = webdriver.Firefox(options=set_options())
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

def scroll_down(driver: webdriver.Firefox, sleep: float = 0.5, popup: dict = None, num_iters: int = 5) -> None:
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
    for _ in range(num_iters):
        html = driver.find_element(By.TAG_NAME, 'html')
        html.send_keys(Keys.END)
        time.sleep(sleep)

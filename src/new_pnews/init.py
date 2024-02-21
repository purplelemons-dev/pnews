from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from time import sleep
from os import makedirs
from os.path import exists
import json
from datetime import datetime as dt

URL = "https://trends.google.com/trends/trendingsearches/realtime?geo=US&hl=en-US&category=all"
BASE = f"./images"

if not exists(BASE):
    makedirs(BASE)


def main():
    options = ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = Chrome(options=options)
    driver.get(URL)

    while True:
        print(f"Getting news at {dt.now()}...")
        driver.get(URL)
        sleep(4)
        out = []
        for idx, i in enumerate(driver.find_elements(By.TAG_NAME, "feed-item")):
            url = i.find_elements(By.TAG_NAME, "a")[-1].get_attribute("href")
            img_name = f"{idx}.png"
            i.screenshot(f"{BASE}/{img_name}")
            out.append(url)
            if idx >= 9:
                break
        with open(f"{BASE}/urls.json", "w") as f:
            json.dump(out, f)
        sleep(55)

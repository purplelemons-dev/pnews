from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from time import sleep

URL = "https://trends.google.com/trends/trendingsearches/realtime?geo=US&hl=en-US&category=all"


def main():
    driver = Chrome()
    driver.get(URL)

    while True:
        sleep(5)
        out = {}
        for i in driver.find_elements(By.TAG_NAME, "feed-item"):
            url = i.find_elements(By.TAG_NAME, "a")[-1].get_attribute("href")
            hashed = hash(url)
            i.screenshot(f"./{hashed}.png")
            out[hashed] = url
        print(out)
        sleep(54)
        driver.refresh()

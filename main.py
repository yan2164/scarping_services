from fastapi import FastAPI
from pydantic import Field
from pydantic.errors import UrlError
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

app = FastAPI()

def getAmazonItem(url):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
    driver.get(url)
    try:
        items = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.ID, "ppd"))
        )
        title = items.find_element_by_xpath('//*[@id="productTitle"]').text
        price_id = ['//*[@id="priceblock_ourprice"]', '//*[@id="corePrice_desktop"]/div/table/tbody/tr/td[2]/span[1]/span[2]', '//*[@id="actualPriceValue"]/strong']
        for id in price_id:
            try:
                price = items.find_element_by_xpath(id).text
            except:
                pass
        img = items.find_element_by_xpath('//*[@id="landingImage"]').get_attribute('src')
        item_list={
            'title' : title,
            'price' : price,
            'img' : img,
        }
        return(item_list)
    finally:
        driver.quit()


def getEbayItem(url):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
    driver.get(url)
    try:
        items = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.ID, "BottomPanelDF"))
        )
        title = items.find_element_by_xpath('//*[@id="itemTitle"]').text
        price_id = ['//*[@id="prcIsum"]', '//*[@id="prcIsum_bidPrice"]', '//*[@id="mm-saleDscPrc"]']
        for id in price_id:
            try:
                price = items.find_element_by_xpath(id).text
            except:
                pass
        img = items.find_element_by_xpath('//*[@id="icImg"]').get_attribute('src')
        item_list={
            'title' : title,
            'price' : price,
            'img' : img,
        }
        return(item_list)
    finally:
        driver.quit()

class Scrape():
    url: str = Field(...,lt=200, description="Paste Amazon or Ebay item's link here")

@app.get("/api/get_data/")
def page(url):
    try:
        if 'www.amazon' in url:
            get_data = getAmazonItem(url)
            return get_data
        elif 'www.ebay' in url:
            get_data = getEbayItem(url)
            return get_data
        else:
            return "url not valid"
    except UrlError as e:
        print(e)
        return e
    
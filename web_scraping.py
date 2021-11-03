from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

url1 ='https://www.amazon.in/Samsung-Galaxy-M12-Storage-Processor/dp/B08XGDN3TZ/ref=lp_1389401031_1_1?dchild=1'
# url2 ='https://www.ebay.com/itm/224516935013?_trkparms=amclksrc%3DITM%26aid%3D111001%26algo%3DREC.SEED%26ao%3D1%26asc%3D20180816085401%26meid%3D7b3283d0ab4f4c45a7ccf01d7ff8e764%26pid%3D100970%26rk%3D2%26rkt%3D3%26sd%3D224306435710%26itm%3D224516935013%26pmt%3D1%26noa%3D1%26pg%3D2380057%26brand%3DUnbranded%2FGeneric&_trksid=p2380057.c100970.m5481&_trkparms=pageci%3Ac03994f1-3c72-11ec-b9ea-426d8af712c2%7Cparentrq%3Ae492f60d17c0a69c39d83066fffe5a7e%7Ciid%3A1'


def checkUrl(url):
    if 'www.amazon' in url:
        getAmazonItem(url)
    elif 'www.ebay' in url:
        getEbayItem(url)
    else:
        msg = "Somthing wnt wrong, try use item's link on Ebay or Amazon"
        return(msg)
    

def getAmazonItem(url):
    s = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=s)
    driver.minimize_window()
    driver.get(url)
    try:
        items = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.ID, "ppd"))
        )
        # print(items.text)
        title = items.find_element_by_xpath('//*[@id="productTitle"]')
        price = items.find_element_by_xpath('//*[@id="priceblock_ourprice"]')
        img = items.find_element_by_xpath('//*[@id="landingImage"]').get_attribute('src')
        # print(title.text)
        # print(price.text)
        # print(img)
        item_list={
            'title' : title.text,
            'price' : price.text,
            'img' : img,
        }
        print(item_list)
        return(item_list)
    finally:
        driver.quit()


def getEbayItem(url):
    s = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=s)
    driver.minimize_window()
    driver.get(url)
    try:
        items = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.ID, "BottomPanelDF"))
        )
        # print(items.text)
        title = items.find_element_by_xpath('//*[@id="itemTitle"]')
        price = items.find_element_by_xpath('//*[@id="prcIsum"]')
        img = items.find_element_by_xpath('//*[@id="icImg"]').get_attribute('src')
        # print(title.text)
        # print(price.text)
        # print(img)
        item_list={
            'title' : title.text,
            'price' : price.text,
            'img' : img,
        }
        print(item_list)
        return(item_list)
    finally:
        driver.quit()

checkUrl('https://www.amazon.com/Mojang-Minecraft/dp/B00992CF6W/ref=lp_9209902011_1_2?dchild=1')
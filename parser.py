from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time


def parse_wildberries(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_driver_path = 'A:/chromedriver/chromedriver.exe'

    service = Service(executable_path=chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.get(url)
    time.sleep(3)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    products = soup.find_all('div', class_='product-snippet')
    result = []

    for product in products:
        product_title = product.find('span', class_='product-card__name').text.strip()
        product_link = product.find('a', class_='product-card__link').get('href')
        old_price = product.find('span', class_='price__old').text.strip()
        current_price = product.find('span', class_='price__lower').text.strip()

        result.append({
            'title': product_title,
            'link': f'https://www.wildberries.by{product_link}',
            'old_price': old_price,
            'current_price': current_price
        })

    driver.quit()
    return result


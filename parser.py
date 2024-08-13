from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time


chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

chrome_driver_path = 'A:/chromedriver/chromedriver.exe'

service = Service(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

url = 'https://www.wildberries.by/catalog/zhenshchinam/odezhda/bluzki-i-rubashki'
driver.get(url)

time.sleep(5)
soup = BeautifulSoup(driver.page_source, 'html.parser')

products = soup.find_all('div', class_='product-snippet')

for product in products:
    product_title = product.find('span', class_='product-card__name').text.strip()
    product_link = product.find('a', class_='product-card__link').get('href')
    old_price = product.find('span', class_='price__old').text.strip()
    current_price = product.find('span', class_='price__lower').text.strip()

    print(f'Название товара: {product_title}')
    print(f'Ссылка на товар: https://www.wildberries.by{product_link}')
    print(f'Цена без скидки: {old_price}')
    print(f'Текущая цена: {current_price}')






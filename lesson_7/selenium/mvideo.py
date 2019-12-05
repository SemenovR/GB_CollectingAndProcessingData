from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from pymongo import MongoClient
import json

chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--no-sandbox")

try:
    client = MongoClient('localhost', 27017)
    db = client.selenium['mvideo']

    driver = webdriver.Chrome(executable_path='./venv/chromedriver', options=chrome_options)
    driver.get('https://www.mvideo.ru/')
    assert "М.Видео" in driver.title

    # Прокручиваем хиты
    while True:
        try:
            # Кнопка прокрутки хитов продаж
            button = WebDriverWait(driver, 10).until(
                ec.presence_of_element_located(
                    (By.XPATH, '//div[contains(text(),"Хиты продаж")]/../../..//a[@class="next-btn sel-hits-button-next"]'))
            )
        except:
            break
        button.send_keys(Keys.RETURN)

    # Получаем список хитов
    li = driver.find_elements(By.XPATH, '//div[contains(text(),"Хиты продаж")]/../../..//li[@class="gallery-list-item"]')
    for l in li:
        # Собираем значения полей
        data = json.loads(l.find_element(By.XPATH, './/a[@class="sel-product-tile-title"]').get_attribute('data-product-info'))
        # Сохраняем значения полей
        db.update_one({'productId': data['productId']}, {'$set': data}, upsert=True)

finally:
    driver.quit()
    client.close()

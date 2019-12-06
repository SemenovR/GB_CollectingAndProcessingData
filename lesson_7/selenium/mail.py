from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from pymongo import MongoClient

chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--no-sandbox")

try:
    client = MongoClient('localhost', 27017)
    db = client.selenium['mail']

    driver = webdriver.Chrome(executable_path='./venv/chromedriver', options=chrome_options)
    wdw = WebDriverWait(driver, 10)

    driver.get('https://mail.ru/?from=logout')
    assert "Mail.ru" in driver.title

    elem = wdw.until(EC.element_to_be_clickable((By.ID, 'mailbox:login')))
    elem.send_keys('test@mail.ru')
    elem.send_keys(Keys.RETURN)
    assert "Mail.ru" in driver.title

    elem = wdw.until(EC.element_to_be_clickable((By.ID, 'mailbox:password')))
    elem.send_keys('testpass')
    elem.send_keys(Keys.RETURN)
    assert "Mail.ru" in driver.title

    # Первое письмо
    elem = wdw.until(EC.presence_of_element_located((By.XPATH, '//a[contains(@class,"llct js-letter-list-item") and contains(@class,"llct_first")]')))
    # Кликаем по письму
    if elem:
        elem.click()

    while elem:
        # Идентификатор письма
        id = elem.get_attribute('data-uidl-id')

        # Ждём пока не прогрузится текст письма
        wdw.until(EC.presence_of_element_located((By.XPATH, f'//div[@data-id="{id}"]')))

        # Собираем значения полей
        try:
            theme = driver.find_element(By.XPATH, '//h2[@class="thread__subject thread__subject_pony-mode"]').text
        except:
            theme = None
        try:
            sender = driver.find_element(By.XPATH, '//div[@class="letter__author"]/span[@class="letter__contact-item"]').text
        except:
            sender = None
        try:
            date = driver.find_element(By.XPATH, '//div[@class="letter__author"]/div[@class="letter__date"]').text
        except:
            date = None
        try:
            text = driver.find_element(By.XPATH, '//div[contains(@id,"_BODY")]/div[contains(@class,"class_")]').text
        except:
            text = None

        # Сохраняем значения полей
        db.update_one({'id': id},
                      {'$set': {'id': id,
                                'sender': sender,
                                'date': date,
                                'theme': theme,
                                'text': text
                                }
                       },
                      upsert=True
                      )

        # Нажимаем кнопку "Вниз" чтобы перейти на следующее письмо
        elem.send_keys(Keys.ARROW_DOWN)
        try:
            # Ждём пока предыдущее письмо не деактивируется
            wdw.until(EC.presence_of_element_located((By.XPATH, f'//a[not(contains(@class,"llct_active")) and @data-uidl-id="{id}"]')))
        except:
            # Если после перехода вниз активное письмо не сменилось, значит просмотрели все письма
            break
        # Берём следующее активное письмо
        elem = wdw.until(EC.presence_of_element_located((By.XPATH, '//a[contains(@class,"llct_active")]')))

finally:
    driver.quit()
    client.close()

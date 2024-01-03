# scroll_times = 10  # Примерное количество прокруток
# scroll_pause_time = 1  # Время ожидания между прокрутками
#
# for _ in range(scroll_times):
#     # Получение информации перед прокруткой
#     elements = driver.find_elements(By.CLASS_NAME, 'wrapper-contain')
#     for el in elements:
#         print(el.text)
#
#     # Прокрутка вниз
#     driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
#
#     # Ожидание загрузки страницы
#     time.sleep(scroll_pause_time)
#
# # Не забывайте закрывать драйвер после завершения работы
# driver.quit()


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time


def parse_stock_atb():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()

    driver.get("https://www.atbmarket.com/catalog/economy/f/discount")

    # Ожидание, пока всплывающее окно станет активным
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.custom-modal__container")))

    # Использование JavaScript для закрытия всплывающего окна
    driver.execute_script("document.querySelector('button.alcohol-modal__submit').click();")
    driver.execute_script("document.querySelector('div.custom-modal__container').remove();")

    # Ожидание 3 секунды, чтобы убедиться, что окно закрылось и сайт отобразился полностью
    time.sleep(3)

    # Теперь сайт должен отображаться нормально
    # Ваш код для работы с сайтом...

    driver.quit()


# Вызываем функцию
# parse_stock_atb()

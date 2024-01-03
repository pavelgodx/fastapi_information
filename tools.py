import time

import aiohttp
from bs4 import BeautifulSoup
import asyncio
from typing import Dict, Union
from fake_useragent import UserAgent
from datetime import datetime
from pathlib import Path
import json
from datetime import datetime, timedelta
import re
from settings import LINKS_KOPEYKA

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options


class AsyncParser:
    def __init__(self, url: str):
        self.url = url
        self.ua = UserAgent()

        self.template_date = "%m/%d/%Y %H:%M"

    def get_config(self) -> Dict[str, str]:
        """
        Generating and returning dictionary of configuration for HTTP request

        Returns:
            Dict[str, str]: dictionary of configuration, where saved information about "user-agent"
        """
        return {'user-agent': self.ua.random}

    async def fetch(self, session: aiohttp.ClientSession, url: str) -> str:
        headers = self.get_config()
        async with session.get(url, headers=headers) as response:
            return await response.text()

    async def format_date(self, value: str) -> str:
        date_obj = datetime.strptime(value, "%B %d, %Y, %H:%M")
        formatted_date = date_obj.strftime(self.template_date)
        return formatted_date

    async def parse_stat(self, text: str):
        try:
            text = int(text)
            return text
        except ValueError:
            return 'no data'

    async def parse_covid_global(self) -> Dict[str, Union[str, int]]:
        async with aiohttp.ClientSession() as session:
            html = await self.fetch(session, 'https://www.worldometers.info/coronavirus/')
            soup = BeautifulSoup(html, 'html.parser')

            update_info_div = soup.find('div', string=lambda x: x and "Last updated:" in x).text.replace(' GMT', '')[
                              14:]

            updated_info_time = await self.format_date(update_info_div)

            covid_cases = soup.find_all('div', class_='maincounter-number')
            covid_cases_amount = int(covid_cases[0].text.replace(',', '').strip())
            covid_death_amount = int(covid_cases[1].text.replace(',', '').strip())
            covid_recovered_amount = int(covid_cases[2].text.replace(',', '').strip())

            return {'last_updated': updated_info_time,
                    'covid_cases': covid_cases_amount,
                    'covid_death': covid_death_amount,
                    'covid_recovered': covid_recovered_amount,
                    'icon': 'cdn-icons-png.flaticon.com/512/2785/2785819.png'
                    }

    async def parce_covid_by_country(self, country: str):
        url = f'https://index.minfin.com.ua/reference/coronavirus/geography/{country}'
        async with aiohttp.ClientSession() as session:
            html = await self.fetch(session, url)
            soup = BeautifulSoup(html, 'html.parser')

            try:
                title_block = soup.find('caption').text
                date_pattern = r'\d{1,2}\.\d{1,2}\.\d{4}'

                date_match = re.search(date_pattern, title_block)
                if date_match:
                    last_updated_date = date_match.group()
                else:
                    last_updated_date = 'no data'

                main_table_block = soup.find('table', 'line main-table')

                population = await self.parse_stat(main_table_block.find_all('strong')[0].text.replace('\xa0', ''))
                total_infections = await self.parse_stat(
                    main_table_block.find_all('strong')[1].text.replace('\xa0', ''))
                deaths = await self.parse_stat(main_table_block.find_all('strong')[2].text.replace('\xa0', ''))
                recovered = await self.parse_stat(main_table_block.find_all('strong')[3].text.replace('\xa0', ''))
                sick_now = await self.parse_stat(main_table_block.find_all('strong')[4].text.replace('\xa0', ''))

                return {'status': 200,
                        'last_updated_date': last_updated_date,
                        'population': population * 1000,
                        'total_infections': total_infections,
                        'deaths': deaths,
                        'recovered': recovered,
                        'sick_now': sick_now}
            except AttributeError:
                return {'status': 'unknown', 'message': 'Error, perhaps the country is missing',
                        'last_updated_date': 'no data'}

    async def parce_currency_list(self):
        url = f'https://www.currency.me.uk/'
        async with aiohttp.ClientSession() as session:
            html = await self.fetch(session, url)
            soup = BeautifulSoup(html, 'html.parser')
            main_block = soup.find('div', class_='content-inner')
            li_tags = main_block.find_all('li')
            data = {}
            for el in li_tags:
                country = el.text
                a_tag = el.find('a')
                if a_tag:
                    currency = a_tag['title']
                    data[country] = currency

            await self.write_to_json('data/currencies/list_of_countries.json', data)

    async def parce_current_currency(self, first_currency: str, second_currency: str):
        url = f'https://www.currency.me.uk/convert/{first_currency}/{second_currency}'
        async with aiohttp.ClientSession() as session:
            html = await self.fetch(session, url)
            if not html:
                return {'status': 'unknown', 'message': 'Error'}
            soup = BeautifulSoup(html, 'html.parser')
            values = soup.find_all('span', class_='mini ccyrate')
            data = {}
            for el in values:
                if 'first_value' not in data:
                    data['first_value'] = el.text
                else:
                    data['second_value'] = el.text
            return data

    async def parse_stock_kopeyka(self):
        for name, link in LINKS_KOPEYKA.items():
            options = Options()
            # options.page_load_strategy = 'eager'  # Не ждать полной загрузки страницы (DOMContentLoaded)

            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)

            driver.get(link)
            product_divs = driver.find_elements(By.CLASS_NAME, 'product.m-t-15')
            data = {}
            for div in product_divs:
                product = div.get_attribute('outerHTML')
                soup = BeautifulSoup(product, 'html.parser')
                prices = soup.find('div', class_='product-price')
                try:
                    new_price = prices.find('div', class_='product-price-new').text.strip()
                    old_price = prices.find('div', class_='product-price-old').text.strip()
                except Exception as e:
                    new_price = None
                    old_price = None

                img_element = soup.find('div', class_='product-img').find('img')
                img_url = img_element['src']
                img_title = img_element['title']

                data[img_title] = {'img_url': img_url, 'old_price': old_price, 'new_price': new_price}

            file_name = f'data/goods/{name}.json'
            await self.write_to_json(file_name, data)

            driver.quit()

    async def write_to_json(self, filename: Union[str, Path], data: Union[str, dict, tuple, list]):
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    async def run(self) -> None:
        data_global_covid = await self.parse_covid_global()
        await self.write_to_json(filename='data/covid/general_info.json', data=data_global_covid)


async def main():  # TODO: убрать
    global_covid_url = 'https://www.worldometers.info/coronavirus/'
    global_covid_object = AsyncParser(global_covid_url)
    await global_covid_object.run()


# asyncio.run(main()) # TODO: доделать


# ---------- OTHER TOOLS ---------- #
async def get_info_from_json(filename: Union[str, Path]):
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)


async def check_elapsed_time(last_updated: str):
    last_updated = datetime.strptime(last_updated, '%m/%d/%Y %H:%M')
    current_time = datetime.now()

    time_difference = current_time - last_updated

    return True if time_difference > timedelta(hours=3) else False


async def check_next_day(last_updated_str: str):
    try:
        last_updated = datetime.strptime(last_updated_str, '%d.%m.%Y').date()
        current_date = datetime.now().date()
        return current_date > last_updated
    except ValueError as e:
        return True

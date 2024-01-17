import aiohttp
from typing import Dict, Union
from fake_useragent import UserAgent
from pathlib import Path
import json
from datetime import datetime, timedelta
import re
from settings import LINKS_KOPEYKA, PRODUCT_NAMES

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
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
        return {'User-Agent': self.ua.random}

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

    async def get_current_date(self):
        current_date = datetime.now()
        formatted_date = current_date.strftime('%d.%m.%Y')
        return formatted_date

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

    async def parce_promotions_atb_store(self):
        main_url = 'https://www.atbmarket.com'
        cur_date = await self.get_current_date()
        data = {'last_updated_date': cur_date}
        id_product = 1
        num_pages = 5

        async with aiohttp.ClientSession() as session:
            for x in range(1, num_pages + 1):
                url = f'https://www.atbmarket.com/ru/promo/economy?page={x}'
                html = await self.fetch(session, url)

                soup = BeautifulSoup(html, 'html.parser')
                main_div = soup.find('div', class_='catalog-list')

                if not main_div:
                    continue

                article_tags = main_div.find_all('article')

                for product in article_tags:
                    if 'banner-item' in product['class']:
                        continue

                    try:
                        block = product.find('div', class_='catalog-item__info')
                        if block:
                            product_name = block.find('a').text.strip()
                            src_picture_url = product.find('img')['src']
                            new_cost = product.find('data', class_='product-price__top').text.strip().split()[0]
                            old_cost = product.find('data', class_='product-price__bottom').text.strip()
                            url_by_product = main_url + product.find('a', class_='catalog-item__photo-link')['href']
                            data[id_product] = {
                                'product_name': product_name, 'new_cost': new_cost, 'old_cost': old_cost,
                                'url_by_product': url_by_product, 'src_picture_url': src_picture_url}
                            id_product += 1
                    except AttributeError as e:
                        print(f'Attribute Error: {e}')
                    except Exception as e:
                        print(f'Unexpected Error: {e}')

        await self.write_to_json('data/products_atb_promotions.json', data)
        return data

    async def write_to_json(self, filename: Union[str, Path], data: Union[str, dict, tuple, list]):
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    async def run(self) -> None:
        data_global_covid = await self.parse_covid_global()
        await self.write_to_json(filename='data/covid/general_info.json', data=data_global_covid)


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

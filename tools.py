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
        async with aiohttp.ClientSession() as session:
            html = await self.fetch(session, f'https://index.minfin.com.ua/reference/coronavirus/geography/{country}')
            soup = BeautifulSoup(html, 'html.parser')

            title_block = soup.find('caption').text
            date_pattern = r'\d{2}\.\d{2}\.\d{4}'

            date_match = re.search(date_pattern, title_block)
            if date_match:
                last_updated_date = date_match.group()
            else:
                last_updated_date = 'no data'

            main_table_block = soup.find('table', 'line main-table')

            population = int(main_table_block.find_all('strong')[0].text.replace('\xa0', ''))
            total_infections = int(main_table_block.find_all('strong')[1].text.replace('\xa0', ''))
            deaths = int(main_table_block.find_all('strong')[2].text.replace('\xa0', ''))
            recovered = int(main_table_block.find_all('strong')[3].text.replace('\xa0', ''))
            sick_now = int(main_table_block.find_all('strong')[4].text.replace('\xa0', ''))

            return {'last_updated_date': last_updated_date,
                    'population': population,
                    'total_infections': total_infections,
                    'deaths': deaths,
                    'recovered': recovered,
                    'sick_now': sick_now}

    async def write_to_json(self, filename: Union[str, Path], data: Union[str, dict, tuple, list]):
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    async def run(self) -> None:
        data_global_covid = await self.parse_covid_global()
        await self.write_to_json(filename='data/covid/general_info.json', data=data_global_covid)


async def main():
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

import aiohttp
from bs4 import BeautifulSoup
import asyncio
from typing import Dict, Union
from fake_useragent import UserAgent
from datetime import datetime


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

    async def fetch(self, session: aiohttp.ClientSession) -> str:
        headers = self.get_config()
        async with session.get(self.url, headers=headers) as response:
            return await response.text()

    async def format_date(self, value: str) -> str:
        date_obj = datetime.strptime(value, "%B %d, %Y, %H:%M")
        formatted_date = date_obj.strftime("%m/%d/%Y %H:%M")
        return formatted_date

    async def parse_covid_global(self) -> Dict[str, Union[str, int]]:
        async with aiohttp.ClientSession() as session:
            html = await self.fetch(session)
            soup = BeautifulSoup(html, 'html.parser')

            update_info_div = soup.find('div', string=lambda x: x and "Last updated:" in x).text.replace(' GMT', '')[
                              14:]

            updated_info_time = await self.format_date(update_info_div)

            covid_cases = soup.find_all('div', class_='maincounter-number')
            covid_cases_amount = int(covid_cases[0].text.replace(',', '').strip())
            covid_death_amount = int(covid_cases[1].text.replace(',', '').strip())
            covid_recovered_amount = int(covid_cases[2].text.replace(',', '').strip())

            return {'last updated': updated_info_time,
                    'covid cases': covid_cases_amount,
                    'covid death': covid_death_amount,
                    'covid recovered': covid_recovered_amount,
                    'source': 'worldometers.info',
                    'icon': 'cdn-icons-png.flaticon.com/512/2785/2785819.png'
                    }

    async def run(self) -> None:
        j = await self.parse_covid_global()
        print(j)


async def main():
    global_covid_url = 'https://www.worldometers.info/coronavirus/'
    global_covid_object = AsyncParser(global_covid_url)
    await global_covid_object.run()


asyncio.run(main())

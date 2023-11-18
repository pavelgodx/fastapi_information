import logging

from fastapi import FastAPI, HTTPException

from tools import get_info_from_json, check_elapsed_time, AsyncParser, check_next_day
from settings import GLOBAL_COVID_TOPIC, COUNTRY_COVID_TOPIC, MAIN_DESCRIPTION
from models import WorldCovidModel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
handler = logging.FileHandler('main_file.log')
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

app = FastAPI(title='PashtetAPI', version='2.2.8', description=MAIN_DESCRIPTION)

global_covid_url = 'https://www.worldometers.info/coronavirus/'
global_covid_object = AsyncParser(global_covid_url)


@app.get('/world/covid', description=GLOBAL_COVID_TOPIC[0], response_model=WorldCovidModel)
async def get_world_covid():
    try:
        data = await get_info_from_json('data/covid/general_info.json')
    except Exception as e:
        logger.error(f"Error occurred: {e}\n\n", exc_info=True)
        raise HTTPException(status_code=500, detail={'status': 'error', 'message': str(e)})
    else:
        if await check_elapsed_time(data['last_updated']):
            new_data = await global_covid_object.parse_covid_global()
            await global_covid_object.write_to_json('data/covid/general_info.json', new_data)
            return new_data
        else:
            return data


@app.get('/world/covid/{country}', description=COUNTRY_COVID_TOPIC)
async def get_covid_info_by_country(country: str):
    json_path = f'data/covid/{country}.json'
    try:
        data = await get_info_from_json(json_path)
    except FileNotFoundError:   # TODO: исправить запись файла jsdklfjdsf.json
        logger.info(f"Data for {country} not found, fetching new data.")
        new_data = await global_covid_object.parce_covid_by_country(country)
        await global_covid_object.write_to_json(f'data/covid/{country}.json', new_data)
        return new_data
    except Exception as e:
        logger.error(f"Error occurred: {e}\n\n", exc_info=True)
        raise HTTPException(status_code=500, detail={'status': 'error', 'message': str(e)})
    else:
        if await check_next_day(data['last_updated_date']): # TODO: здесь также траблы
            logger.info(f"Data for {country} is outdated, fetching new data.")
            new_data = await global_covid_object.parce_covid_by_country(country)
            await global_covid_object.write_to_json(json_path, new_data)
            return new_data
        else:
            return data

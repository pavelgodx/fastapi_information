from typing import List
from fastapi import FastAPI, HTTPException
from tools import get_info_from_json
from settings import GLOBAL_COVID_TOPIC
from models import WorldCovidModel

from fastapi import FastAPI, Request, Header
from babel import Locale, negotiate_locale
from babel.support import Translations
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
handler = logging.FileHandler('main_file.log')
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

app = FastAPI()


@app.get('/world/covid', description=GLOBAL_COVID_TOPIC[0], response_model=WorldCovidModel)
async def get_world_covid():
    try:
        data = await get_info_from_json('data/covid/genhjkheral_info.json')
        return data
    except Exception as e:
        logger.error(f"Error occurred: {e}\n\n", exc_info=True)

        raise HTTPException(status_code=500, detail={'status': 'error', 'message': str(e)})

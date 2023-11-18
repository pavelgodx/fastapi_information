from typing import List
from fastapi import FastAPI
from tools import get_info_from_json
from settings import GLOBAL_COVID_TOPIC
from models import WorldCovidModel

from fastapi import FastAPI, Request, Header
from babel import Locale, negotiate_locale
from babel.support import Translations

app = FastAPI()


@app.get('/world/covid', description=GLOBAL_COVID_TOPIC[0], response_model=WorldCovidModel)
async def get_world_covid():
    data = await get_info_from_json('data/covid/general_info.json')
    return data

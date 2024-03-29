import logging
from fastapi import FastAPI, HTTPException
from tools import get_info_from_json, check_elapsed_time, AsyncParser, check_next_day
from settings import (GLOBAL_COVID_DESCRIPTION, COUNTRY_COVID_DESCRIPTION, MAIN_DESCRIPTION, TAGS, SUMMARY,
                      GET_CURRENCY_TOPIC, CURRENCY_LIST_TOPIC)
from models import WorldCovidModel, CurrencyModel

app = FastAPI(title='PashtetAPI', version='2.2.8', description=MAIN_DESCRIPTION)

global_covid_url = 'https://www.worldometers.info/coronavirus/'
tool_object = AsyncParser(global_covid_url)


@app.get('/world/covid', description=GLOBAL_COVID_DESCRIPTION, response_model=WorldCovidModel, tags=TAGS[0],
         summary=SUMMARY[0])
async def get_world_covid():
    try:
        data = await get_info_from_json('data/covid/general_info.json')
    except FileNotFoundError:
        new_data = await tool_object.parse_covid_global()
        await tool_object.write_to_json('data/covid/general_info.json', new_data)
        data = await get_info_from_json('data/covid/general_info.json')
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail={'status': 'error', 'message': str(e)})
    else:
        if await check_elapsed_time(data['last_updated']):
            new_data = await tool_object.parse_covid_global()
            await tool_object.write_to_json('data/covid/general_info.json', new_data)
            return new_data
        else:
            return data


@app.get('/world/covid/{country}', description=COUNTRY_COVID_DESCRIPTION, tags=TAGS[0], summary=SUMMARY[1])
async def get_covid_info_by_country(country: str):
    json_path = f'data/covid/{country}.json'
    try:
        data = await get_info_from_json(json_path)
    except FileNotFoundError:
        new_data = await tool_object.parce_covid_by_country(country)
        if new_data['status'] != 200:
            return new_data
        await tool_object.write_to_json(f'data/covid/{country}.json', new_data)
        return new_data
    except Exception as e:
        raise HTTPException(status_code=500, detail={'status': 'error', 'message': str(e)})
    else:
        if await check_next_day(data['last_updated_date']):  # TODO: здесь также траблы
            new_data = await tool_object.parce_covid_by_country(country)
            if new_data['status'] != 200:
                return new_data
            await tool_object.write_to_json(json_path, new_data)
            return new_data
        # else:
        #     return data


@app.get('/currency/list', description=CURRENCY_LIST_TOPIC, tags=TAGS[1], summary=SUMMARY[2])
async def get_list_currencies():
    # await tool_object.parce_currency_list() ---> get actually list currencies
    data = await get_info_from_json('data/currencies/list_of_countries.json')
    return data


@app.get('/currency/{first_currency}/{second_currency}', description=GET_CURRENCY_TOPIC, tags=TAGS[1],
         summary=SUMMARY[3], response_model=CurrencyModel)
async def get_current_currency(first_currency: str, second_currency: str):
    new_data = await tool_object.parce_current_currency(first_currency.lower(), second_currency.lower())
    return new_data


@app.get('/atb/promotions')  # TODO: добавить модель
async def get_promotions_atb_store():
    json_path = 'data/goods/products_atb_promotions.json'
    data = await get_info_from_json(json_path)
    if await check_next_day(data['last_updated_date']):
        data = await tool_object.parce_promotions_atb_store()  # TODO: MAKE EXCEPTIONS!
        await tool_object.write_to_json(json_path, data)

    return data

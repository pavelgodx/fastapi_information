from pydantic import BaseModel, Field
from typing import Dict


class WorldCovidModel(BaseModel):
    last_updated: str = Field(example='12/25/1998 14:08')
    covid_cases: int = Field(example=697961377)
    covid_death: int = Field(example=6939360)
    covid_recovered: int = Field(example=669531101)
    icon: str = Field(example='example.com/picture.png')


class CurrencyModel(BaseModel):
    first_value: str = Field(example='1 USD = 38.1502 UAH')
    second_value: str = Field(example='1 UAH = 0.0262 USD')


class PromotionsKopeika(BaseModel):
    TheProductName: Dict[str, str] = Field(..., example={
        'img_url': 'example.com/somepicture.png',
        'old_price': '10.7грн.',
        'new_price': '8.50грн.'
    })
    TheProductName2: Dict[str, str] = Field(..., example={
        'img_url': 'example.com/somepicture2.png',
        'old_price': '25.12грн.',
        'new_price': '12.25грн.'
    })

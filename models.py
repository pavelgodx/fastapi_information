from pydantic import BaseModel, Field, HttpUrl
from typing import Dict, List


class WorldCovidModel(BaseModel):
    last_updated: str = Field(example='12/25/1998 14:08')
    covid_cases: int = Field(example=697961377)
    covid_death: int = Field(example=6939360)
    covid_recovered: int = Field(example=669531101)
    icon: str = Field(example='example.com/picture.png')


class CurrencyModel(BaseModel):
    first_value: str = Field(example='1 USD = 38.1502 UAH')
    second_value: str = Field(example='1 UAH = 0.0262 USD')


# class ProductDetails(BaseModel):
#     img_url: HttpUrl = Field(..., example="https://example.com/image.png")
#     old_price: str = Field(..., example="3948uah")
#     new_price: str = Field(..., example="3222uah")
#
# class ProductsModel(ProductDetails):
#     products: List[str, img_url]


from pydantic import BaseModel, Field


class WorldCovidModel(BaseModel):
    last_updated: str = Field(example='12/25/1998 14:08')
    covid_cases: int = Field(example=697961377)
    covid_death: int = Field(example=6939360)
    covid_recovered: int = Field(example=669531101)
    source: str = Field(example='example.com')
    icon: str = Field(example='example.com/picture.png')

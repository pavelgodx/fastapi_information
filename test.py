import pytest
from tools import AsyncParser, check_next_day


@pytest.mark.asyncio
async def test_parce_covid_by_country():
    parser = AsyncParser("https://index.minfin.com.ua/reference/coronavirus/geography/")
    result = await parser.parce_covid_by_country('usa')
    print('\n', result)

    assert 'status' in result
    assert result['status'] == 200

@pytest.mark.asyncio
async def test_parse_stock_kopeyka():
    parser = AsyncParser('some_url')
    await parser.parse_stock_kopeyka()

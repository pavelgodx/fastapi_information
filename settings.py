GLOBAL_COVID_TOPIC = (
    'Get information about the number of people affected by COVID 19. Data is updated every 3 hours.',
)

COUNTRY_COVID_TOPIC = """
We receive information about COVID-19 for the specified country. Supported countries:
- Ukraine
- USA
- Canada
- Germany
- France
- Russia

"""

CURRENCY_LIST_TOPIC = """
Получи весь список данных
"""

GET_CURRENCY_TOPIC = """
Ееее бой!
"""

ATB_STOCK_TOPIC = """
Получи все акции товаров
"""

MAIN_DESCRIPTION = ('This API will help you obtain up-to-date information from various sources. '
                    'Repository in [GitHub](https://github.com/pavelgodx/fastapi_information). '
                    '\n\nAlso for feedback: [telegram](https://t.me/pavelgodx)'
                    '\n\n![lol](https://media.tenor.com/tWD3GjJcoHgAAAAC/spongebob-computer.gif)')

TAGS = [
    ['Covid'],
    ['Currency'],
    ['Stock'],
]

SUMMARY = ('Get world COVID info',
           'Get COVID info by country',
           'Get list currencies',
           'Get current exchange rate',
           'Get current shares in Kopeyka',)

LINKS_KOPEYKA = {
    'alcohol': 'https://my.kopeyka.com.ua/shares/category/9?name=%D0%90%D0%BB%D0%BA%D0%BE%D0%B3%D0%BE%D0%BB%D1%8C',
    'grocer': 'https://my.kopeyka.com.ua/shares/category/21?name=%D0%91%D0%B0%D0%BA%D0%B0%D0%BB%D0%B5%D1%8F',
    'hygiene': 'https://my.kopeyka.com.ua/shares/category/1?name=%D0%93%D0%B8%D0%B3%D0%B8%D0%B5%D0%BD%D0%B0',
    'for_kids': 'https://my.kopeyka.com.ua/shares/category/22?name=%D0%94%D0%BB%D1%8F%20%D0%B4%D0%B5%D1%82%D0%B5%D0%B9',
    'freezing': 'https://my.kopeyka.com.ua/shares/category/24?name=%D0%97%D0%B0%D0%BC%D0%BE%D1%80%D0%BE%D0%B7%D0%BA%D0%B0',
    'yoghurts': 'https://my.kopeyka.com.ua/shares/category/27?name=%D0%99%D0%BE%D0%B3%D1%83%D1%80%D1%82%D1%8B',
    'sausages': 'https://my.kopeyka.com.ua/shares/category/3?name=%D0%9A%D0%BE%D0%BB%D0%B1%D0%B0%D1%81%D1%8B',
    'conservation': 'https://my.kopeyka.com.ua/shares/category/4?name=%D0%9A%D0%BE%D0%BD%D1%81%D0%B5%D1%80%D0%B2%D0%B0%D1%86%D0%B8%D1%8F',
    'cooking': 'https://my.kopeyka.com.ua/shares/category/20?name=%D0%9A%D1%83%D0%BB%D0%B8%D0%BD%D0%B0%D1%80%D0%B8%D1%8F',
    'dairy': 'https://my.kopeyka.com.ua/shares/category/5?name=%D0%9C%D0%BE%D0%BB%D0%BE%D0%BA%D0%BE%20%D0%AF%D0%B9%D1%86%D0%B0',
    'seafood': 'https://my.kopeyka.com.ua/shares/category/6?name=%D0%9C%D0%BE%D1%80%D0%B5%D0%BF%D1%80%D0%BE%D0%B4%D1%83%D0%BA%D1%82%D1%8B',
    'ice_cream': 'https://my.kopeyka.com.ua/shares/category/7?name=%D0%9C%D0%BE%D1%80%D0%BE%D0%B6%D0%B5%D0%BD%D0%BD%D0%BE%D0%B5',
    'meat_products': 'https://my.kopeyka.com.ua/shares/category/19?name=%D0%9C%D1%8F%D1%81%D0%BD%D1%8B%D0%B5%20%D0%B8%D0%B7%D0%B4%D0%B5%D0%BB%D0%B8%D1%8F',
    'cookies': 'https://my.kopeyka.com.ua/shares/category/29?name=%D0%9F%D0%B5%D1%87%D0%B5%D0%BD%D1%8C%D0%B5',
    'dishes': 'https://my.kopeyka.com.ua/shares/category/8?name=%D0%9F%D0%BE%D1%81%D1%83%D0%B4%D0%B0',
    'sweets': 'https://my.kopeyka.com.ua/shares/category/16?name=%D0%A1%D0%BB%D0%B0%D0%B4%D0%BE%D1%81%D1%82%D0%B8',
    'snacks': 'https://my.kopeyka.com.ua/shares/category/14?name=%D0%A1%D0%BD%D0%B5%D0%BA%D0%B8',
    'juices_water': 'https://my.kopeyka.com.ua/shares/category/15?name=%D0%A1%D0%BE%D0%BA%D0%B8%20%D0%92%D0%BE%D0%B4%D1%8B',
    'sauces': 'https://my.kopeyka.com.ua/shares/category/17?name=%D0%A1%D0%BE%D1%83%D1%81%D1%8B',
    'cheese': 'https://my.kopeyka.com.ua/shares/category/13?name=%D0%A1%D1%8B%D1%80',
    'cottage_cheese': 'https://my.kopeyka.com.ua/shares/category/26?name=%D0%A2%D0%B2%D0%BE%D1%80%D0%BE%D0%B3',
    'chemistry': 'https://my.kopeyka.com.ua/shares/category/10?name=%D0%A5%D0%B8%D0%BC%D0%B8%D1%8F',
    'tea_coffee': 'https://my.kopeyka.com.ua/shares/category/18?name=%D0%A7%D0%B0%D0%B9%20%D0%9A%D0%BE%D1%84%D0%B5'

}

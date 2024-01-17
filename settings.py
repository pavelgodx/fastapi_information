# ------------------------------ MAIN INFO ------------------------------ #

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
           'Get current promotions in Kopeyka',)

# ------------------------------ COVID ------------------------------ #

GLOBAL_COVID_DESCRIPTION = """
### Get information about the number of people affected by COVID 19. Data is updated every ~3 hours.

- Total cases
- Deaths
- Recovered
"""

COUNTRY_COVID_DESCRIPTION = """
### We receive information about COVID-19 for the specified country. Supported countries:
- Ukraine
- USA
- Canada
- Germany
- France
- Russia
"""

# ------------------------------ CURRENCY ------------------------------ #


CURRENCY_LIST_TOPIC = """
### Data about some countries and their currencies in XXX format (UAH, USD, etc.)
"""

GET_CURRENCY_TOPIC = """
### Current data on average currency exchange rates.
"""

# ------------------------------ PROMOTIONS  ------------------------------ #


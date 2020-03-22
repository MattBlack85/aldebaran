from starlette.routing import Mount, Route

from .views import (
    countries,
    countries_by_day,
    countries_by_month,
    country,
    list_countries,
    regions,
    regions_by_date,
    totals,
)

api_routes = [
    Mount(
        '/api',
        routes=[
            Route('/countries', countries, methods=['GET']),
            Route('/countries/by_date/day/{day}', countries_by_day, methods=['GET']),
            Route('/countries/by_date/month/{month}', countries_by_month, methods=['GET']),
            Route('/countries/{country}', country, methods=['GET']),
            Route('/list_countries', list_countries, methods=['GET']),
            Route('/totals', totals, methods=['GET']),
            Route('/regions/totals', regions, methods=['GET']),
            Route('/regions', regions_by_date, methods=['GET']),
        ],
    )
]

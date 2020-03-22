import json
from datetime import datetime as dt

from starlette.responses import JSONResponse

from .queries import (
    all_data_query,
    countries_by_day_query,
    countries_by_month_query,
    country_data_query,
    country_list_query,
    latest_data_by_region_query,
    latest_data_query,
    region_data_by_day_query,
)


async def totals(request):
    result = await request.app.state.database.fetch_all(query=latest_data_query)
    prepared_data = [
        {
            'country': r['country'],
            'total_cases': int(r['total_cases']),
            'total_deaths': int(r['total_deaths']),
        }
        for r in result
    ]
    return JSONResponse(prepared_data)


async def countries(request):
    result = await request.app.state.database.fetch_all(query=all_data_query)
    prepared_data = [{r['country']: json.loads(r['data'])} for r in result]
    return JSONResponse(prepared_data)


async def list_countries(request):
    result = await request.app.state.database.fetch_all(query=country_list_query)
    prepared_data = [r['country'] for r in result]
    return JSONResponse(prepared_data)


async def country(request):
    country = request.path_params['country']
    if '_' in country:
        country = country.replace('_', ' ')
    result = await request.app.state.database.fetch_all(
        query=country_data_query, values={'country': country}
    )
    prepared_data = [
        {
            'date': r['report_datetime'].date().isoformat(),
            'total_deaths': int(r['total_deaths']),
            'new_deaths': int(r['new_deaths']),
            'total_cases': int(r['total_cases']),
            'new_cases': int(r['new_cases']),
        }
        for r in result
    ]
    return JSONResponse(prepared_data)


async def countries_by_day(request):
    try:
        day = dt.strptime(request.path_params['day'], '%Y_%m_%d')
    except ValueError:
        return JSONResponse({'error': 'BAD_FORMAT_DATE'}, status_code=400)

    if not day:
        return JSONResponse(status_code=404)

    result = await request.app.state.database.fetch_all(
        query=countries_by_day_query, values={'day': day}
    )
    prepared_data = [
        {
            'country': r['country'],
            'total_cases': int(r['total_cases']),
            'new_cases': int(r['new_cases']),
            'total_deaths': int(r['total_deaths']),
            'new_deaths': int(r['new_deaths']),
        }
        for r in result
    ]
    return JSONResponse(prepared_data)


async def countries_by_month(request):
    try:
        month = dt.strptime(request.path_params['month'], '%Y_%m')
    except ValueError:
        return JSONResponse({'error': 'BAD_FORMAT_DATE'}, status_code=400)

    result = await request.app.state.database.fetch_all(
        query=countries_by_month_query, values={'month': month.month}
    )
    prepared_data = [
        {
            'country': r['country'],
            'total_cases': int(r['tc']),
            'new_cases': int(r['nc']),
            'total_deaths': int(r['td']),
            'new_deaths': int(r['nd']),
        }
        for r in result
    ]
    return JSONResponse(prepared_data)


async def regions(request):
    result = await request.app.state.database.fetch_all(query=latest_data_by_region_query)
    prepared_data = [
        {
            'region': r['region'],
            'total_deaths': int(r['total_deaths']),
            'total_cases': int(r['total_cases']),
        }
        for r in result
    ]
    return JSONResponse(prepared_data)


async def regions_by_date(request):
    result = await request.app.state.database.fetch_all(query=region_data_by_day_query)
    prepared_data = [
        {
            'region': r['region'],
            'total_deaths': int(r['total_deaths']),
            'total_cases': int(r['total_cases']),
            'date': r['time'].date().isoformat(),
        }
        for r in result
    ]
    return JSONResponse(prepared_data)

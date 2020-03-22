import pytest


def test_get_country_all_data(test_client):
    """
    There are 53 entries for China in the test DB
    """
    response = test_client.get('api/countries/China')
    assert len(response.json()) == 53


def test_get_all_countries_data(test_client):
    """
    There are 223 total entries in the test DB and 5 countries in total
    """
    response = test_client.get('api/countries')
    assert len(response.json()) == 5
    total_entries = []
    for country in response.json():
        for entry in list(country.values())[0]:
            total_entries.append(entry)

    assert len(total_entries) == 223


def test_list_countries(test_client):
    response = test_client.get('api/list_countries')
    assert len(response.json()) == 5


@pytest.mark.parametrize('date', ['2020_10_00', '2020_01_XX', '20200123'])
def test_get_data_by_day_bad_day(test_client, date):
    response = test_client.get(f'api/countries/by_date/day/{date}')
    assert response.status_code == 400


@pytest.mark.parametrize('date', ['2020_44', '2020_00', '202001'])
def test_get_data_by_month_bad_month(test_client, date):
    response = test_client.get(f'api/countries/by_date/month/{date}')
    assert response.status_code == 400


@pytest.mark.parametrize('date', ['2020_1', '2020_01'])
def test_get_data_by_month_ok(test_client, date):
    response = test_client.get(f'api/countries/by_date/month/{date}')
    assert response.status_code == 200

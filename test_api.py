import api
import pytest


@pytest.fixture
def client():
    test_client = api.application.test_client()
    return test_client


# Helper Function
# Gets REST data as json
def get_response_as_json(client, url):
    get_request = client.get(url)
    return get_request.get_json()


# Test the get request on /api/weather
# returns all of the forecasts
def test_all_weather_get(client):
    response = get_response_as_json(client, '/api/weather')
    assert len(response) == 7


# Test the get request on /api/weather
# with argument begin /api/weather?begin=<val>
def test_weather_arg_begin_get(client):
    response = get_response_as_json(
            client, 
            '/api/weather?begin="2018-08-23 21:27:49"'
            )
    assert len(response) == 4


# Test the get request on /api/weather
# with argument end /api/weather?end=<val>
def test_weather_arg_end_get(client):
    response = get_response_as_json(
            client, 
            '/api/weather?end="2018-08-23 21:27:49'
            )
    assert len(response) == 3


# Test the get request on /api/weather
# with booth begin and end 
# /api/weather?begin=<val1>&end=<val2>
def test_weather_arg_booth_get(client):
    response = get_response_as_json(
            client,
            '/api/weather?begin="2018-08-22"&end="2018-08-24"'
            )
    assert len(response) == 6


# Test the get request on /api/weather/recent
# Checks that it returns the exact json response
def test_recent_weather_get(client):
    response = get_response_as_json(client, '/api/weather/recent')
    recent = {
        'id': 7,
        'date_time': '2018-08-28 15:44:55.904761',
        'humidity': 0.6,
        'wetness': 145,
        'wind_speed': 0.0,
        'temperature': 91.99,
        'pressure': 42.11
    }
    assert response == recent


# Test a Exception on /api/weather
# Checks if a message is sent if
# a bad query is made in the request
def test_weather_DataError(client):
    response = client.get('/api/weather?begin="dfsd"')
    message = {
        'message': ("The browser (or proxy) sent"
                    " a request that this server could"
                    " not understand."
                    )
    }
    assert response.status_code == 400
    assert response.get_json() == message


import api


def test_all_weather_get():
    app = api.application.test_client()
    response = app.get('/api/weather')
    assert len(response.get_json()) == 7


def test_weather_DataError():
    app = api.application.test_client()
    response = app.get('/api/weather?begin="dfsd"')
    message = {
        'message': ("The browser (or proxy) sent"
                    " a request that this server could"
                    " not understand."
                    )
    }
    assert response.status_code == 400
    assert response.get_json() == message


def test_weather_arg_begin_get():
    app = api.application.test_client()
    response = app.get('/api/weather?begin="2018-08-23 21:27:49"')
    assert len(response.get_json()) == 4


def test_weather_arg_end_get():
    app = api.application.test_client()
    response = app.get('/api/weather?end="2018-08-23 21:27:49')
    assert len(response.get_json()) == 3


def test_weather_arg_booth_get():
    app = api.application.test_client()
    response = app.get('/api/weather?begin="2018-08-22"&end="2018-08-24"')
    assert len(response.get_json()) == 6


def test_recent_weather_get():
    app = api.application.test_client()
    response = app.get('/api/weather/recent')
    recent = {
        'id': 7,
        'date_time': '2018-08-28 15:44:55.904761',
        'humidity': 0.6,
        'wetness': 145,
        'wind_speed': 0.0,
        'temperature': 91.99,
        'pressure': 42.11
    }
    assert response.get_json() == recent

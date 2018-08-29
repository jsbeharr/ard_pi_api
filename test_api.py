import api
import requests
import json


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

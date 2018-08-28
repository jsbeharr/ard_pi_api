from flask import Flask, jsonify
from flask_restful import Resource, Api, fields, marshal
from flask_sqlalchemy import SQLAlchemy
import json

application = Flask(__name__)
api = Api(application)

# Configures application from a config.cfg
application.config.from_pyfile('config.cfg')
db = SQLAlchemy(application)

weather_fields = {
            'id': fields.Integer,
            'date_time' : fields.DateTime,
            'humidity' : fields.Float,
            'wetness' : fields.Integer,
            'wind_speed' : fields.Float,
            'temperature' : fields.Float,
            'pressure': fields.Float
        }

class Weather_forecasts(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    date_time = db.Column(db.DateTime, nullable=False)
    humidity = db.Column(db.Float, nullable=False)
    wetness = db.Column(db.Integer, nullable=False)
    wind_speed = db.Column(db.Float, nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    pressure = db.Column(db.Float, nullable=False)


class AllWeather(Resource):
    def get(self):
        return {'weather': [marshal(weather, weather_fields) for weather in Weather_forecasts.query.all()]}

class RecentWeather(Resource):
    def get(self):
        return {'weather': [marshal(weather, weather_fields) for weather in Weather_forecasts.query.order_by(Weather_forecasts.date_time.desc()).limit(1)]}

api.add_resource(AllWeather, '/api/weather')
api.add_resource(RecentWeather, '/api/weather/recent')


if __name__ == '__main__':
    application.run(debug=True)

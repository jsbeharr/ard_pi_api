from flask import Flask, request
from flask_restful import Resource, Api, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize Flask and API
application = Flask(__name__)
api = Api(application)

# Configures application from a config.cfg
application.config.from_pyfile('config.cfg')
db = SQLAlchemy(application)

# Data fields for Weather Object
weather_fields = {
        'id': fields.Integer,
        'date_time' : fields.DateTime,
        'humidity' : fields.Float,
        'wetness' : fields.Integer,
        'wind_speed' : fields.Float,
        'temperature' : fields.Float,
        'pressure': fields.Float
        }

# Weather Forecast Model
# Contains columns for all of the weather data
class Weather_forecasts(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    date_time = db.Column(db.DateTime, nullable=False)
    humidity = db.Column(db.Float, nullable=False)
    wetness = db.Column(db.Integer, nullable=False)
    wind_speed = db.Column(db.Float, nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    pressure = db.Column(db.Float, nullable=False)


# Resource getting all of the weather
class AllWeather(Resource):
    @marshal_with(weather_fields)
    def get(self):
        try:
            # url arguments do "/weather?<arg1>=<val1>&<arg2>=<val2>&..."
            # or just do "/weather" to get all data
            date_begin = request.args.get('begin', default='2018-06-27', type=str)
            date_end = request.args.get('end', default=datetime.now(), type=str)
            return Weather_forecasts.query.filter(Weather_forecasts.date_time.between(date_begin, date_end)).all()
        except Exception as e:
            return {'error' : str(e) }
        

# Resource getting the most recent weather report
class RecentWeather(Resource):
    @marshal_with(weather_fields)
    def get(self):
        try:
            return Weather_forecasts.query.order_by(Weather_forecasts.id.desc()).first()
        except Exception as e:
            return {'error' : str(e) }

# API URLS
# Visit urls to fetch data
api.add_resource(AllWeather, '/api/weather')
api.add_resource(RecentWeather, '/api/weather/recent')


if __name__ == '__main__':
    application.run(debug=True)

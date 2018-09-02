from flask import Flask, request, abort, render_template
from flask_restful import Resource, Api, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from flask_misaka import Misaka
from sqlalchemy.exc import OperationalError, DataError
from mdx_gfm import GithubFlavoredMarkdownExtension
from datetime import datetime
import markdown

# Initialize Flask and API
application = Flask(__name__, template_folder='templates')
api = Api(application)

# Allow application to use markdown
Misaka(application)

# Configures application from a config.cfg
application.config.from_pyfile('config.cfg')
db = SQLAlchemy(application)

# Data fields for Weather Object
weather_fields = {
    'id': fields.Integer,
    'date_time': fields.String,
    'humidity': fields.Float,
    'wetness': fields.Integer,
    'wind_speed': fields.Float,
    'temperature': fields.Float,
    'pressure': fields.Float
}


class Weather_forecasts(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    date_time = db.Column(db.String, nullable=False)
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
            date_begin = request.args.get(
                'begin',
                default='2018-06-27',
                type=str)
            date_end = request.args.get(
                'end',
                default=datetime.now(),
                type=str)
            # query weather data
            forecasts = Weather_forecasts.query \
                .filter(
                    Weather_forecasts.date_time.between(
                        date_begin,
                        date_end
                    )
                ).all()
            # checks if any forecasts were collected
            if forecasts is not None:
                return forecasts
            else:
                return {}
        except DataError:
            abort(400, DataError.statement)
        except OperationalError:
            abort(500, OperationalError.statement)


# Resource getting the most recent weather report
class RecentWeather(Resource):
    @marshal_with(weather_fields)
    def get(self):
        try:
            return Weather_forecasts.query \
                .order_by(
                    Weather_forecasts.id.desc()
                ).first()
        except DataError:
            abort(400, DataError.statement)
        except OperationalError:
            abort(500, OperationalError.statement)


@application.route('/')
def index():
    # content = ''
    # with open('readme.md', 'r') as f:
    #     content = f.read()
    #     md = markdown.Markdown(extensions=[GithubFlavoredMarkdownExtension()])
    #     content = md.convert(content)
    return render_template('index.html')


# API URLS
# Visit urls to fetch data
api.add_resource(AllWeather, '/api/weather')
api.add_resource(RecentWeather, '/api/weather/recent')


if __name__ == '__main__':
    application.run(debug=True)

from flask import Flask, jsonify
from flask_restful import Resource, Api, fields, marshal
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)
api = Api(app)

# Configures app from a config.cfg
app.config.from_pyfile('config.cfg')
db = SQLAlchemy(app)

class Weather_forecasts(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    date_time = db.Column(db.DateTime, nullable=False)
    humidity = db.Column(db.Float, nullable=False)
    wetness = db.Column(db.Integer, nullable=False)
    wind_speed = db.Column(db.Float, nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    pressure = db.Column(db.Float, nullable=False)

    def __repr__(self):
        data = {
            'id': self.id,
            'date_time' : self.date_time,
            'humidity' : self.humidity,
            'wetness' : self.wetness,
            'wind_speed' : self.wind_speed,
            'temperature' : self.temperature,
            'pressure': self.pressure
        }
        return json.dumps(data)



class HelloWorld(Resource):
    def get(self):
        weather_fields = {
            'id': fields.Integer,
            'date_time' : fields.DateTime,
            'humidity' : fields.Float,
            'wetness' : fields.Integer,
            'wind_speed' : fields.Float,
            'temperature' : fields.Float,
            'pressure': fields.Float
        }
        return {'weather': [marshal(weather, weather_fields) for weather in Weather_forecasts.query.all()]}

api.add_resource(HelloWorld, '/')


if __name__ == '__main__':
    app.run(debug=True)

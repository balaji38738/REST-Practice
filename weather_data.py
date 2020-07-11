from flask_restful import Resource, Api
from flask import Flask, request
import requests
import json
import csv
import os

app = Flask(__name__)
api = Api(app)

class WeatherReport(Resource):
    def put(self):
        zipcode = request.form["zip"]
        response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?zip={zipcode},"
                    + "in&appid={os.environ['apiid']}")
        json_object = response.json()
        with open('weather_report.json', 'w') as json_file:
            json.dump(json_object, json_file)
        return json_object


api.add_resource(WeatherReport, '/weather')

if __name__ == '__main__':
    app.run(debug=True)
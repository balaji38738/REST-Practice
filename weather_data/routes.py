from flask_restful import Resource
from flask import request, jsonify, make_response
from weather_data import api, db
import requests
import json
import csv
import os
from weather_data import app
import asyncio
import csv
from weather_data.models import Weather
import datetime

loop = asyncio.get_event_loop()

class WeatherReport(Resource):
    def put(self):
        zipcode = request.form["zip"]
        response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?zip={zipcode},in&appid={os.environ['apiid']}")
        json_object = response.json()
        time = datetime.datetime.now()
        longitude = json_object['coord']['lon']
        latitude = json_object['coord']['lat']
        description = json_object['weather'][0]['description']
        temp_min = json_object['main']['temp_min']
        temp_max = json_object['main']['temp_max']
        pressure = json_object['main']['pressure']
        humidity = json_object['main']['humidity']
        windspeed = json_object['wind']['speed']
        weather_data = {'time':time, 'longitude':longitude, 'latitude':latitude,
                        'description':description, 'temp_min':temp_min,
                        'temp_max':temp_max, 'pressure':pressure,
                        'humidity':humidity, 'windspeed':windspeed
                        }
        loop.run_until_complete(add_weather_data(weather_data))
        loop.close()
        return make_response(json_object, 404)

api.add_resource(WeatherReport, '/weather')

async def add_weather_data(weather_data):
    task1 = loop.create_task(insert_to_db(weather_data))
    task2 = loop.create_task(add_to_csv_file(weather_data))
    await asyncio.wait([task1, task2])

async def insert_to_db(weather_data):
    new_entry = Weather(time=weather_data['time'], longitude=weather_data['longitude'], latitude=weather_data['latitude'],
                        description=weather_data['description'], temp_min=weather_data['temp_min'],
                        temp_max=weather_data['temp_max'], pressure=weather_data['pressure'],
                        humidity=weather_data['humidity'], windspeed=weather_data['windspeed'])
    db.create_all()
    db.session.add(new_entry)
    await asyncio.sleep(2)
    db.session.commit()

async def add_to_csv_file(weather_data):
    with open('weather_report.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        if os.stat('weather_report.csv').st_size == 0:
            writer.writerow(list(weather_data.keys()))
        writer.writerow(list(weather_data.values()))
        await asyncio.sleep(2)


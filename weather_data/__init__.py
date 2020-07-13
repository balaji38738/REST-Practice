from flask_restful import Api
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
api = Api(app, catch_all_404s=True)
app.config["SECRET_KEY"] = os.environ['weather_api_secret']
mysql_password = os.environ["mysql_password"]
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://root:{mysql_password}@localhost/weather_db?charset=utf8mb4'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
from weather_data import db

class Weather(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.column(db.DateTime)
    longitude = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(20), nullable=False)
    temp_min = db.Column(db.Float, nullable=False)
    temp_max = db.Column(db.Float, nullable=False)
    pressure = db.Column(db.Float, nullable=False)
    humidity = db.Column(db.Float, nullable=False)
    windspeed = db.Column(db.Float, nullable=False)
    

import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################

@app.route("/")
def welcome():
    return (
        f"Welcome to the SurfsUp in Hawaii API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start>"
         f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
 
    session = Session(engine)
    
    results = session.query(Measurement.date,Measurement.prcp).all()

    session.close()

    precipitation = []
    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict["Date"] = date
        precipitation_dict["Precipitation"] = prcp
        precipitation.append(precipitation_dict)

    return jsonify(precipitation)


@app.route("/api/v1.0/station")
def station():
   
    session = Session(engine)
    
    results = session.query(Station.station,Station.name).all()

    session.close()

    station = []
    for station, name in results:
        station_dict = {}
        station_dict["Station"] = station
        station_dict["Name"] = name
        precipitation.append(station_dict)

    return jsonify(station)

@app.route("/api/v1.0/tobs")
def temperature():

    session = Session(engine)
    
    query_date_12_months = dt.date(2016, 8, 17) 
    results = session.query(Measurement.station, Measurement.date, Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        order_by(Measurement.date.asc()).\
            filter(func.strftime(Measurement.date) > query_date_12_months).all()
    
    session.close()

    temperature = []
    for date, tobs in results:
        temperature_dict = {}
        temperature_dict["Date"] = date
        temperature_dict["Temperature"] = tobs
        precipitation.append(temperature_dict)
        
    return jsonify(temperature)

if __name__ == '__main__':
    app.run(debug=True)

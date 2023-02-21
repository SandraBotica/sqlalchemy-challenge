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
        f"Enter start date"
        f"(start date must be in YYYY-MM-DD format)<br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
 
    session = Session(engine)
    
    precipitation = session.query(Measurement.date,Measurement.prcp).all()

    session.close()

    results = list(np.ravel(precipitation))
    
    # precipitation_list = []
    # for date, prcp in results:
    #     precipitation_dict = {}
    #     precipitation_dict["Date"] = date
    #     precipitation_dict["Precipitation"] = prcp
    #     precipitation.append(precipitation_dict)
    # return jsonify(precipitation_list)
    return jsonify(results)


@app.route("/api/v1.0/station")
def stations():
   
    session = Session(engine)
    
    stations = session.query(Station.station,Station.name).all()

    session.close()

    results = list(np.ravel(stations))
    
    # station_name = []
    # for station, name in results:
    #     station_dict = {}
    #     station_dict["Station"] = station
    #     station_dict["Name"] = name
    #     precipitation.append(station_dict)
    # return jsonify(station_name)
    return jsonify(results)

@app.route("/api/v1.0/tobs")
def temperature():

    query_date_12_months = dt.date(2016, 8, 17) 
    
    session = Session(engine)
    
    temperature = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        order_by(Measurement.date.asc()).\
        filter(func.strftime(Measurement.date) > query_date_12_months).all()
    
    session.close()
    
    results = list(np.ravel(temperature))

    # temperature = []
    # for date, tobs in results:
    #     temperature_dict = {}
    #     temperature_dict["Date"] = date
    #     temperature_dict["Temperature"] = tobs
    #     precipitation.append(temperature_dict)
    # return jsonify(temperature)
    
    return jsonify(results)

@app.route("/api/v1.0/<start>")
def starting_date(start):
    
    session = Session(engine)
    
    starting_date = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    
    session.close()
    
    results = list(np.ravel(starting_date))
    
    return jsonify(results)

@app.route("/api/v1.0/<start>/<end>")
def starting_end_date(start,end):
    
    session = Session(engine)
    
    starting_end_date = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).\
            filter(Measurement.date <= end).all()
    
    session.close()
    
    results = list(np.ravel(starting_end_date))
    
    return jsonify(results)



if __name__ == '__main__':
    app.run(debug=True)

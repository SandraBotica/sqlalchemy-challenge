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
# Displaying Available routes on landing page
@app.route("/")
def welcome():
    return (
        f"Welcome to the SurfsUp in Hawaii API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"Enter a start date in YYYY-MM-DD format after/<br/>"
        f"/api/v1.0/<start><br/>"
        f"Enter a start date in YYYY-MM-DD format after the first/ and an end date after the second/<br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )
# Creating precipitation route 
# Converting query into a dictionary with date as the key and precipitation as the value
# Filtering for just last 12 months of precipitation values
# Returning json representation of the dictionary

@app.route("/api/v1.0/precipitation")
def precipitation():
 
    session = Session(engine)
    
    date_12_months = dt.date(2016, 8, 22) 
    
    precipitations = session.query(Measurement.date,Measurement.prcp).\
        order_by(Measurement.date.asc()).\
        filter(func.strftime(Measurement.date) > date_12_months).all()

    session.close()
    
    precipitation_list = []
    for date, prcp in precipitations:
        precipitation_dict = {date:prcp}
        precipitation_list.append(precipitation_dict)
    return jsonify(precipitation_list)

# Creating stations route 
# Converting query into a list of station id's and the station name
# Returning json representation of the list

@app.route("/api/v1.0/stations")
def stations():
   
    session = Session(engine)
    
    stations_query = session.query(Station.station,Station.name).all()

    session.close()

    results = list(np.ravel(stations_query))
    
    return jsonify(results)

# Creating temperature route 
# Converting query into a list of temperatures for the most active station
# Filtering for just last 12 months of temperature values
# Returning json representation of the list

@app.route("/api/v1.0/tobs")
def temperature():
    
    session = Session(engine)
    
    query_date_12_months = dt.date(2016, 8, 17) 
    
    temperature_query = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        order_by(Measurement.date.asc()).\
        filter(func.strftime(Measurement.date) > query_date_12_months).all()
    
    session.close()
    
    results = list(np.ravel(temperature_query))
    
    return jsonify(results)

# Creating a route for a <start date> to be entered
# Converting query into a list of min, max and average temperatures 
# Filtering for temperature values from entered <start date> to last date in dataset
# Returning json representation of the list

@app.route("/api/v1.0/<start><br/>")
def starting_date(start):

    """Fetch the temperatures from start date matches to last date of dataset 
    as a path variable supplied by the user, or a 404 if not."""
     
    session = Session(engine)
    
    start = ()
    
    starting_date_list = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    
    session.close()
    
    date_list= []
    for min, max, avg in starting_date_list:
        temp_list = [min,max,avg]
        date_list.append(temp_list)

    # return jsonify({"error": f"Start date {start} not found."}), 404
   
    # results = list(np.ravel(starting_date_list))
    
    return jsonify(date_list)

# Creating a route for a <start date> and <end> to be entered
# Converting query into a list of min, max and average temperatures 
# Filtering for temperature values from entered <start date> to <end>
# Returning json representation of the list

# @app.route("/api/v1.0/<start>/<end><br/>")
# def starting_end_date(start,end):
    
#     session = Session(engine)
    
#     start = dt.date("<start>")
#     end = dt.date("<end>")
    
#     starting_end_date_list = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
#         filter(Measurement.date >= start).\
#             filter(Measurement.date <= end).all()
    
#     session.close()
    
#     results = list(np.ravel(starting_end_date_list))
    
#     return jsonify(results)



if __name__ == '__main__':
    app.run(debug=True)

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
        f"Using the route below<br/>"
        f"Enter a start date in YYYYMMDD format after/<br/>"
        f"The start date can be between 20100101-20170823<br/>"
        f"This will display the min, average and max value of temperature from the start date to 20170823<br/>"
        f"/api/v1.0/<start><br/>"
        f"Using the route below<br/>"
        f"Enter a start date in YYYYMMDD format after the first/ and an end date after the second/<br/>"
        f"The start and end date can be between 20100101-20170823<br/>"
        f"This will display the min, average and max value of temperature from the start to end date<br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )
# Creating precipitation route 
# Converting query into a dictionary with date as the key and precipitation as the value
# Filtering for just last 12 months of precipitation values
# Returning json representation of the dictionary

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
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
    # Create our session (link) from Python to the DB
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
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    query_date_12_months = dt.date(2016, 8, 17) 
    
    temperature_query = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        order_by(Measurement.date.asc()).\
        filter(func.strftime(Measurement.date) > query_date_12_months).all()
    
    session.close()
    
    results = list(np.ravel(temperature_query))
    
    return jsonify(results)

# Creating a route for a <start> date to be entered
# Converting query into a list of min, max and average temperatures 
# Filtering for temperature values from entered <start> date to last date in dataset
# Returning json representation of the list

@app.route("/api/v1.0/<start>")
def starting_date(start):

    """Fetch the temperatures from start date entered to last date of dataset 
    as a path variable supplied by the user."""
    
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    start=dt.datetime.strptime(start, "%Y%m%d")
    
    starting_date_list = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    
    session.close()
   
    results = list(np.ravel(starting_date_list))
    
    return jsonify(results)
    # return jsonify({f"The min temp: " (results)[0][0], "The average temp: " (results)[0][1],"The max temp: " (results)[0][2]})
    

# Creating a route for a <start> date and <end> date to be entered
# Converting query into a list of min, max and average temperatures 
# Filtering for temperature values from entered <start> to <end> date
# Returning json representation of the list

@app.route("/api/v1.0/<start>/<end>")
def starting_end_date(start,end):
    
    """Fetch the temperatures from start to end date of dataset 
    as a path variable supplied by the user."""
    
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    start=dt.datetime.strptime(start, "%Y%m%d")
    end=dt.datetime.strptime(end, "%Y%m%d")
    
    starting_end_date_list = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).\
            filter(Measurement.date <= end).all()
    
    session.close()
    
    results = list(np.ravel(starting_end_date_list))
    
    return jsonify(results)
    # return jsonify({f"The Min, Average and Max temperature for the date range selected is {results}"})



if __name__ == '__main__':
    app.run(debug=True)

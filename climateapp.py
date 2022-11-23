import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify

engine = create_engine("sqlite:///titanic.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)

measurement = Base.classes.measurement
station = Base.classes.station

app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of precipitation"""
    session.query(measurement.date).order_by(measurement.date.desc()).first()
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    rain = session.query(measurement.date, measurement.prcp).filter(measurement.date > query_date)
    for measurement in rain:
        print(measurement.date, measurement.prcp)
        results = session.query(measurement.prcp).all()

    session.close()

     # Create a dictionary from the row data and append to a list of all_passengers
    precipitation = []
    for name, age, sex in results:
        passenger_dict = {}
        passenger_dict["name"] = name
        passenger_dict["age"] = age
        passenger_dict["sex"] = sex
        precipitation.append(passenger_dict)

    return jsonify(results)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of stations from the dataset"""
    # Query all stations
    results = session.query(station.station).all()

    session.close()

    return jsonify(results)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Query the dates and temperature observations of the most-active station for the previous year of data"""
    # Query temperature observations
    session.query(measurement.date).order_by(measurement.date.desc()).first()
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(measurement.date, measurement.tobs).filter(measurement.station == 'USC00519281').filter(measurement.date >= query_date).all()

    session.close()

    return jsonify(results)

@app.route("/api/v1.0/<start>")
def start():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date"""
    # Query temperature for start date
    start_temp = session.query(func.min(measurement.tobs),func.max(measurement.tobs),func.avg(measurement.tobs)).filter(measurement.date == '2016-08-02').all()
    session.close()

    return jsonify(start_temp)

@app.route("/api/v1.0/<start>/<end>")
def start_to_end():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive"""
    # Query temperature for start date to end date
    end_temp = session.query(func.min(measurement.tobs),func.max(measurement.tobs),func.avg(measurement.tobs)).filter(measurement.date ==< '2016-08-02' and ==> '2017-08-02').all()
    session.close()

    return jsonify(end_temp)

if __name__ == '__main__':
    app.run(debug=True)
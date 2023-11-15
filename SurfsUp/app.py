# Import the dependencies.
from sqlite3 import Date
from flask import Flask, jsonify
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func
import datetime as dt

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///../Resources/hawaii.sqlite", echo=False)

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect = True)

# Save references to each table
Measurement = Base.classes.measurement
Stations = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)
#################################################
# Set Query logic
#################################################
latest_date = session.query(Measurement.date).\
                        order_by(Measurement.date.desc()).\
                        limit(1).all()[0][0]

a_year_ago = dt.datetime.strptime(latest_date,'%Y-%m-%d') - dt.timedelta(days=366)

prcp_data = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date > a_year_ago).\
        order_by(Measurement.date).all()

stations_app_data = session.query(Stations.station, Stations.name, Stations.latitude, Stations.longitude)

most_active = session.query(Measurement.station, func.count(Measurement.station)).\
            group_by(Measurement.station).\
            order_by(func.count(Measurement.station).desc()).all()

top_most_active = most_active[0][0]

top_data =  session.query(Measurement.station, Measurement.tobs).\
    filter(Measurement.date <= latest_date).\
    filter(Measurement.date >= a_year_ago).\
    filter(Measurement.station==top_most_active)

session.close()
#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
#Landing route
@app.route("/")
def Home():
    return (
        f"Welcome!<br/>"
        f"Copy and paste one of the following routes,<br/>"
        f"to look at the different analysis:<br/>"
        f"* Precipitations:<br/>"
        f"   /api/v1.0/precipitation<br/>"
        f'* Stations: <br/>'
        f'   /api/v1.0/stations<br/>'
        f'* Temperatures: <br/>'
        f'   /api/v1.0/tobs<br/>'
    )

#Precipitations route
@app.route("/api/v1.0/precipitation")
def Precipitations_app():
    prcp_list = []
    for date, pcrp  in prcp_data:
            prcp_dict = {}
            prcp_dict[f'{date}'] = pcrp
            prcp_list.append(prcp_dict)


    return jsonify(prcp_list)

#Stations route
@app.route("/api/v1.0/stations")
def Stations_app():
    stations_list = []
    for station, name, latitude, longitud in stations_app_data:
            stations_dict = {}
            stations_dict[f'Station'] = station
            stations_dict[f'Name'] = name
            stations_dict[f'Latitude'] = latitude
            stations_dict[f'Longitude'] = longitud
            stations_list.append(stations_dict)


    return jsonify(stations_list)
    
#Most Active Station Temperature route:
@app.route("/api/v1.0/tobs")
def Temperature_app():
    temp_list = []
    for date, tobs in top_data:
            temp_dict = {}
            temp_dict[f'Date'] = date
            temp_dict[f'TOBS'] = tobs
            temp_list.append(temp_dict)


    return jsonify(temp_list)


# 4. Define main behavior
if __name__ == "__main__":
    app.run(debug=True)
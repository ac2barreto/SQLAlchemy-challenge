from sqlite3 import Date
from flask import Flask, jsonify
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func
import datetime as dt

engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

Base = automap_base()

Base.prepare(autoload_with=engine)

Measurement = Base.classes.measurement
Stations = Base.classes.stationsession=Session(engine)

stations_app_data = session.query(Stations.station, Stations.name, Stations.latitude, Stations.longitude)

latest_date = session.query(Measurement.date).\
                        order_by(Measurement.date.desc()).\
                        limit(1).all()[0][0]

a_year_ago = dt.datetime.strptime(latest_date,'%Y-%m-%d') - dt.timedelta(days=366)

prcp_data = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date > a_year_ago).\
        order_by(Measurement.date).all()

most_active = session.query(Measurement.station, func.count(Measurement.station)).\
            group_by(Measurement.station).\
            order_by(func.count(Measurement.station).desc()).all()

top_most_active = most_active[0][0]

top_data =  session.query(Measurement.station, Measurement.tobs).\
    filter(Measurement.date >= a_year_ago).\
    filter(Measurement.station==top_most_active)


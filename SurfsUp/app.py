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


# reflect an existing database into a new model

# reflect the tables


# Save references to each table


# Create our session (link) from Python to the DB
session = Session(engine)
#################################################
# Flask Setup
#################################################




#################################################
# Flask Routes
#################################################


import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
from datetime import datetime


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################
todaydate = datetime.now()
oneyearback = todaydate.replace(year=todaydate.year-1).strftime("%Y-%m-%d")
oneyearback = "2017-06-03"

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/tobs<br/>"
        f"//api/v1.0/<start> and /api/v1.0/<start>/<end><br/>"
        f"/api/v1.0/stations"
    )


@app.route("/api/v1.0/precipitation")
def names():
    df2 = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= oneyearback).all()
    lst = {}
    for x in df2:
        #print(x[0])
        lst[x[0]] = x[1]
    print(lst)
    return jsonify(lst)


@app.route("/api/v1.0/stations")
def stations():
    df2 = session.query(Station.id,Station.station,Station.name,Station.latitude,Station.longitude,Station.elevation).all()
    lst = {}
    for x in df2:
        #print(x[0])
        #lst[x[1]] = [x[2],x[3],x[4],x[5]]
        lst[x[1]] = {"name":x[2],"latitude":x[3],"longitude":x[4],"elevation":x[5]}
    #print(lst)
    return jsonify(lst)

@app.route("/api/v1.0/tobs")
def tobs():
    df2 = session.query(Measurement.tobs).filter(Measurement.date >= oneyearback).all()
    lst = []
    for x in df2:
        lst.append(x[0])

    return jsonify(lst)


@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def justice_league_character2(start,end=False):
    """Return a list of passenger data including the name, age, and sex of each passenger"""
    # Query all passengers
    sql = "SELECT MAX(`tobs`), MIN(`tobs`), AVG(`tobs`), `date` FROM `measurement` WHERE"
    if end == False:
        sql += " `date`='"+str(start)+"'"
        df2 = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs), Measurement.date).group_by(Measurement.date).filter(Measurement.date >= start).all()
    else:
        sql += " `date` > '"+str(start)+"' AND `date` < '"+str(end)+"'"
        df2 = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs), Measurement.date).group_by(Measurement.date).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    sql += " GROUP BY `date`"
    #df2 = engine.execute(sql).fetchall()
    print(df2)
    lst = []
    for x in df2:
        l = {
            "date":x[3],
            "max":x[0],
            "min":x[1],
            "avg":x[2]
        }
        lst.append(l)
    #print(lst)
    return jsonify(lst)


if __name__ == '__main__':
    app.run(debug=True)

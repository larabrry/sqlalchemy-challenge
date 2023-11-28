# Import the dependencies.
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, distinct
from flask import Flask, jsonify
import numpy as np


#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
base= automap_base()
# reflect the tables
base.prepare(autoload_with=engine) #(engine, reflect=True)?????

# Save references to each table
Measurement = base.classes.measurement
Station = base.classes.station

# Create our session (link) from Python to the DB
session= Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################
#List all the available routes.
@app.route("/")                
def home():
    """List all available api routes"""
    return (
        f"Welcome to the Home Page API!<br/>"
        f"Available Routes for Hawaii Weather:<br/>"
        f"/<br/>"
        f"http://127.0.0.1:5000/<br/>"
        f"http://127.0.0.1:5000/api/v1.0/latest_date <br/>"
        f"http://127.0.0.1:5000/api/v1.0/precipitation<br/>"
        f"http://127.0.0.1:5000/api/v1.0/stations<br/>"
        f"http://127.0.0.1:5000/api/v1.0/active_stations<br/>"
        f"http://127.0.0.1:5000/api/v1.0/tobs<br/>"
        f"http://127.0.0.1:5000/api/v1.0/<start><br/>"
        f"http://127.0.0.1:5000/api/v1.0/<start>/<end><br/>"
    ) 




#Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data)
# to a dictionary using date as the key and prcp as the value.
#Return the JSON representation of your dictionary.
    

@app.route("/api/v1.0/latest_date")
def get_latest_date():
    recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    rs={"recent_date": recent_date[0]}
    session.close()
    return jsonify(rs)

def get_start_date():
    recent_date= get_latest_date().json.get("recent_date")
    latest_date= recent_date.split("-")
    start_year= int(latest_date[0])-1
    start_date= str(start_year)+"-"+latest_date[1]+"-"+latest_date[2]
    return {"start_date":start_date}

@app.route("/api/v1.0/precipitation")
def precipitation(): 
    start_date=get_start_date()
    sel = [Measurement.date, Measurement.prcp]    
    precipitation = session.query(*sel).\
        filter(func.strftime(Measurement.date) >= start_date['start_date']).all()
    session.close()
    preci_dict= dict()
    for date, prcp in precipitation:
        if preci_dict.get(date)is None:
            preci_dict[date]=[]
        preci_dict[date].append(prcp)
    return jsonify(preci_dict)
   

#Return a JSON list of stations from the dataset.

@app.route("/api/v1.0/stations")
def station():
    """Return a list of all the stations in Hawaii"""
    list_stations= session.query(Station.station).all()
    session.close()
    list_of_stations = list(np.ravel(list_stations)) 
    return jsonify(list_of_stations)
    
@app.route("/api/v1.0/active_stations")
def get_active_stations():
    sel = [Measurement.station, 
       func.count(Measurement.station)]
    active_stations = session.query(*sel).\
        group_by(Measurement.station).\
        order_by(func.count(Measurement.station).desc()).all()
    session.close()
    active_stations_data= [] 
    for station, count in active_stations:
        active_stations_data.append({"station":station, "count": count})
    
    return jsonify(active_stations_data)

#Query the dates and temperature observations of the most-active station for the previous year of data.
#Return a JSON list of temperature observations for the previous year.

@app.route("/api/v1.0/tobs")
def tobs():
    
    m_station= get_active_stations().json[0]['station']
    sel = [Measurement.date, Measurement.tobs]
    station_temps = session.query(*sel).\
        filter(func.strftime(Measurement.date) >= get_start_date()["start_date"], Measurement.station == m_station).\
        group_by(Measurement.date).\
        order_by(Measurement.date).all()
    session.close()
    mactive_tobs_dict= dict()
    for date, observation in station_temps:
        if mactive_tobs_dict.get(date)is None:
            mactive_tobs_dict[date]=observation
        #mactive_tobs_dict[date].append(observation)
        
    return jsonify(mactive_tobs_dict)
     
 

#Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.
#For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.
#For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.

@app.route("/api/v1.0/<start>" )
def start (start):
    result = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).first() 
    session.close()
    temps=dict()
    temps['TMIN']=result[0]
    temps['TAVG']=result[1]
    temps['TMAX']=result[2]
 
    if temps['TMIN']:
        return jsonify(temps)
    else:
        return jsonify({"error": f"Date {start} not found or not formatted as YYYY-MM-DD."}), 404

@app.route("/api/v1.0/<start>/<end>")
def start_end (start, end):
    result = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).first()
    session.close()
    temps=dict()
    temps['TMIN']=result[0]
    temps['TAVG']=result[1]
    temps['TMAX']=result[2]

    if temps['TMIN']: 
        return jsonify(temps)
    else:
        return jsonify({"error": f"Date {start} or {end} not found or not formatted as YYYY-MM-DD."}), 404
    
     

if __name__ == "__main__":
    app.run(debug=True)

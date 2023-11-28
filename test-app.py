
import requests

res=requests.get("http://127.0.0.1:5000/")
print("/",res)
res=requests.get("http://127.0.0.1:5000/api/v1.0/latest_date ")
print("latest_date",res,res.json,res.text)
res=requests.get("http://127.0.0.1:5000/api/v1.0/precipitation")
print("precipitation",res,res.json,res.text)
res=requests.get("http://127.0.0.1:5000/api/v1.0/stations")
print("stations",res,res.json,res.text)
res=requests.get("http://127.0.0.1:5000/api/v1.0/active_stations")
print("active_stations",res,res.json,res.text)
res=requests.get("http://127.0.0.1:5000/api/v1.0/tobs")
print("tobs", res,res.json,res.text)
res=requests.get("http://127.0.0.1:5000/api/v1.0/2016-08-23")
print("start",res,res.json,res.text)
res=requests.get("http://127.0.0.1:5000/api/v1.0/2016-08-23/2017-08-23")
print("start/send",res,res.json,res.text)

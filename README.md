# Sqlalchemy Challenge

Congratulations! You've decided to treat yourself to a long holiday vacation in Honolulu, Hawaii. To help with your trip planning, you decide to do a climate analysis about the area.

## Part 1: Analyze and Explore the Climate Data
- Use the file [hawaii.sqlite](https://github.com/larabrry/sqlalchemy-challenge/blob/main/Resources/hawaii.sqlite) to complete the climate analysis and data exploration.
1. Use the SQLAlchemy ```create_engine()``` function to connect to your SQLite database.

2. Use the SQLAlchemy ```automap_base()``` function to reflect your tables into classes, and then save references to the classes named station and measurement.

3. Link Python to the database by creating a SQLAlchemy session.

- Perform a precipitation analysis and then a station analysis

## Part 2: Design Your Climate App

- After completing the initial data analysis, design a Flask API based on the queries that were just developed.

1. ``/``

- Start at the homepage and list all the available routes.
- I made a route for each query I've used in the data analysis.
2. ```/api/v1.0/precipitation```

- Convert the query results from the precipitation analysis to a dictionary using date as the key and prcp as the value.

- Return the JSON representation of your dictionary.

 - I decided to create a ```get_latest_date``` and a ```get_start_date``` method and adding their queries to separate routes first. 
- I also used the ```get_start_date``` method to filter the start date in the precipitation query instead of entering it manually. 

3. ```/api/v1.0/stations```

- Return a JSON list of stations from the dataset.
- I have also included a JSON dictionary including the active stations and their counts by creating a ```get_active_stations``` method under a separate ```"/api/v1.0/active_stations"``` route. 

4. ```/api/v1.0/tobs```

- Query the dates and temperature observations of the most-active station for the previous year of data.
- Return a JSON list of temperature observations for the previous year.
- Here I've also used the the ```get_start_date```and  ```get_active_stations``` method to filter the most- active station in the query instead of typing it manually. 

5. ```/api/v1.0/<start>``` and ```/api/v1.0/<start>/<end>```

- Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.

- For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.

- For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.




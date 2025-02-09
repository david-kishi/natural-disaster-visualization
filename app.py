from flask import Flask, render_template, redirect, request, jsonify
from flask_pymongo import PyMongo
from bson.json_util import dumps
    

#Create an instance for Flask
app = Flask(__name__)

#Use Pymongo to establish Mongo Connection
mongo = PyMongo(app, uri = "mongodb://localhost:27017/weather_data")


#Route to render index.html template using data from Mongo
@app.route("/")
def index():
    
    return render_template("index.html")

@app.route('/<disaster_type>') 
def natural_disaster(disaster_type):
    if disaster_type == 'flood':
        data = dumps(mongo.db.flood_data.find())
        return  (data)
    
    elif disaster_type == 'earthquake':
        data = dumps(mongo.db.earthquake_data.find())
        return  (data)
    
    elif disaster_type == "hurricane":
        data = dumps(mongo.db.hurricane_data.find())
        return  (data)
    
    elif disaster_type == 'tornado':
        data = dumps(mongo.db.tornado_data.find())
        return  (data)
    
    else:
        return jsonify({'ok': False, 'message': 'Bad request parameters!'})

@app.route('/<disaster_type>/<myyear>') 
def natural_disaster_years(disaster_type,myyear):
    if disaster_type == 'flood':
        data = dumps(mongo.db.flood_data.find({"year": int(myyear)}))
        # count = dumps(mongo.db.flood_data.find({"year": int(myyear)}).count())
        return  (data)
        # return (count)

    
    elif disaster_type == 'earthquake':
        data = dumps(mongo.db.earthquake_data.find({"year": int(myyear)}))
        return  (data)
    
    elif disaster_type == "hurricane":
        data = dumps(mongo.db.hurricane_data.find({"year": int(myyear)}))
        return  (data)
    
    elif disaster_type == 'tornado':
        data = dumps(mongo.db.tornado_data.find({"year": int(myyear)}))
        return  (data)
    
    else:
        return jsonify({'ok': False, 'message': 'Bad request parameters!'})

@app.route('/<disaster_type>/<s_year>/<e_year>') 
def natural_disaster_time_frame(disaster_type,s_year,e_year):
    if disaster_type == 'floods':
        data = dumps(mongo.db.flood_data.find({"year": {"$gte":int(s_year),"$lte":int(e_year)}}))
        return  (data)
    
    elif disaster_type == 'earthquakes':
        data = dumps(mongo.db.earthquake_data.find({"year": {"$gte":int(s_year),"$lte":int(e_year)}}))
        return  (data)
    
    elif disaster_type == "hurricane":
        data = dumps(mongo.db.hurricane_data.find({"year": {"$gte":int(s_year),"$lte":int(e_year)}}))
        return  (data)
    
    elif disaster_type == 'tornado':
        data = dumps(mongo.db.tornado_data.find({"year": {"$gte":int(s_year),"$lte":int(e_year)}}))
        return  (data)
    
    else:
        return jsonify({'ok': False, 'message': 'Bad request parameters!'})

@app.route('/<year>/counts')
def natural_disaster_years_count(year):
    counts = {
        "eCount": dumps(mongo.db.earthquake_data.find({"year": int(year)}).count()),
        "fCount": dumps(mongo.db.flood_data.find({"year": int(year)}).count()),
        "tCount": dumps(mongo.db.tornado_data.find({"year": int(year)}).count()),
        "hCount": dumps(mongo.db.hurricane_data.find({"year": int(year)}).count())
    }
    
    return jsonify(counts)

# Function to return dictionary of counts of entries by month
def count_months(disaster,year):
    months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    temp_list = []

    for month in months:
        temp_list.append(dumps(mongo.db[f'{disaster}_data'].find({"year": int(year), "month": month}).count()))

    return temp_list


@app.route('/<year>/counts/month')
def natural_disaster_months_count(year):
    counts = {
        "earthquake": count_months("earthquake", year),
        "flood": count_months("flood", year),
        "tornado": count_months("tornado", year),
        "hurricane": count_months("hurricane", year),
    }

    return jsonify(counts)


if __name__ == "__main__":
    app.run(debug=True)

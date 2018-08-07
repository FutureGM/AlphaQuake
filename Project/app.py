import pandas as pd
import numpy as np
import os
import pymongo
import json
import flask
import geojson

from flask import Flask, render_template
from flask import Flask, Response
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo
from bson import json_util
from bson.json_util import dumps
from geojson import Feature, FeatureCollection, Point


uri_key = os.environ.get("uri")
app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'earthquake'
app.config['MONGO_URI'] = uri_key



mongo = PyMongo(app)

@app.route('/')
def main():
    return render_template("landingpage.html")

@app.route("/dataVisualization")
def dataVisualization():
    return render_template('heatmap_2.html')

@app.route("/earthquakedata")
def earthquakedata():
    connection = pymongo.MongoClient(uri_key)
    collection = connection["earthquake"]["all_records"]
    projects = collection.find({},{"_id":False}).limit(100)
    json_projects = []
    data = {
        "type": "FeatureCollection",
        "features": [
        {
            "type": "Feature",

            "properties" : {"mag":[d["mag"]], "place":[d["place"]], "date":[d["Date"]]},

            "geometry" : {
                "type": "Point",
                "coordinates": [d["longitude"], d["latitude"]],
                },
        } for d in projects]
    }
    json_projects.append(data)
    return jsonify(data)


#@app.route("/earthquakemachine")
#def earthquakemachine():
#    connection = pymongo.MongoClient(uri)
#    collection = connection["earthquake"]["all_records"]
#    projects = collection.find({},{"_id":False}).limit(100)
#    json_projects = []
#    data = {
#        "type": "FeatureCollection",
#        "features": [
#        {
#            "type": "Feature",
#
#            "properties" : {"mag":[d["mag"]], "place":[d["place"]], "date":[d["Date"]]},
#
#            "geometry" : {
#                "type": "Point",
#                "coordinates": [d["longitude"], d["latitude"]],
#                },
#        } for d in projects]
#    }
#    json_projects.append(d)
#    return Response(
#        json_projects, 
#        mimetype="text/json", 
#        headers={"Content-Disposition":"attachment;filename=data.json"})
#    
    
@app.route("/d3atlas")
def d3page():
    return render_template("d3Atlas.html")

@app.route("/scatterplot")
def scatterplot():
    return render_template("scatter.html")

if __name__ == "__main__":
    app.run()
#
#if __name__ == "__main__":
#    filepath = os.path.join("mlData.json")
#    earthquakemachine(filepath)
#    app.run()





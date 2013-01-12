#! /usr/bin/env python
# -*- coding: utf-8 -*-

from models import *

from flask import jsonify, render_template, request

def toDictList(list):
    return [e.toDict() for e in list]

def toGeoJSONFeatureCollectionDict(features):
    return {
            'type': 'FeatureCollection',
            'features': [f.toGeoJSONDict() for f in features]
            }
# site

@app.route("/")
def index():
    return render_template("map.html")

@app.route("/agencies")
def agencies():
    return render_template("agencies.html")

# api

# agencies

@app.route('/api/agencies')
def api_agencies():
    agencies = Agency.query.all()
    return jsonify(agencies = toDictList(agencies))

@app.route('/api/agencies/<int:id>')
def api_agencies_id(id):
    agency = Agency.query.filter(Agency.id == id).first()
    if agency:
        return jsonify(agency.toDict())
    else:
        return jsonify(error="Agency not found."), 404

# stops

@app.route('/api/stops')
def api_stops():
    stops = Stop.query.limit(100)
    if request.args.get('asGeoJSON'):
        return jsonify(toGeoJSONFeatureCollectionDict(stops))
    else:
        return jsonify(stops = toDictList(stops))

@app.route('/api/stops/<int:id>')
def api_stops_id(id):
    stop = Stop.query.filter(Stop.id == id).first()
    if stop:
        if request.args.get('asGeoJSON'):
            return jsonify(stop.toGeoJSONDict())
        else:
            return jsonify(stop.toDict())
    else:
        return jsonify(error="Stop not found."), 404

# trips

@app.route('/api/trips')
def api_trips():
    trips = Trip.query.all()
    return jsonify(trips = toDictList(trips))

@app.route('/api/trips/<int:id>')
def api_trips_id(id):
    trip = Trip.query.filter(Trip.id == id).first()
    if trip:
        return jsonify(trip.toDict())
    else:
        return jsonify(error="Stop not found."), 404

# transfer

@app.route('/api/transfers')
def api_transfer():
    transfers = Transfer.query.all()
    return jsonify(transfers = toDictList(transfers))

@app.route('/api/transfers/<int:from_stop_id>/<int:to_stop_id>')
def api_transfer_from_to(from_stop_id, to_stop_id):
    transfer = Transfer.query.filter(Transfer.from_stop_id == from_stop_id) \
            .filter(Transfer.to_stop_id == to_stop_id).first()
    if transfer:
        return jsonify(transfer.toDict())
    else:
        return jsonify(error="Transfer not found."), 404



if __name__ == '__main__':
    app.run(debug=True)

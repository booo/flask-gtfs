#! /usr/bin/env python
# -*- coding: utf-8 -*-

from models import *

from flask import jsonify, render_template, request

from sqlalchemy import or_

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

@app.route("/trips")
def trips():
    return render_template("trips.html")

@app.route("/trips/<int:id>")
def trip(id):
    trip = Trip.query.get_or_404(id)
    return render_template("trip.html", trip = trip)

@app.route("/agencies")
def agencies():
    return render_template("agencies.html")

@app.route("/agencies/<int:id>")
def agencies_id(id):
    agency = Agency.query.get_or_404(id)
    return render_template("agency.html", agency = agency)

@app.route("/routes")
def routes():
    return render_template("routes.html")

@app.route("/routes/<int:id>")
def route(id):
    route = Route.query.get_or_404(id)
    return render_template("route.html", route = route)

@app.route("/linegraph")
def linegraph():
    return render_template("linegraph.html")

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

# shapes

@app.route('/api/shapes')
def api_shapes():

    shapes = None

    bbox = request.args.get('bbox')
    if bbox:
        east, north, west, south = bbox.split(",")
        #TODO remove sql injection?
        bbox = "POLYGON(({} {}, {} {}, {} {}, {} {}, {} {}))".format(north, east, \
                north, west, south, west, south, east, north, east)
        shapes = Shape.query.filter(Shape.geometry.intersects(bbox))
    else:
        shapes = Shape.query.all()

    if request.args.get('asGeoJSON'):
        return jsonify(toGeoJSONFeatureCollectionDict(shapes))
    else:
        return jsonify(shapes = toDictList(shapes))

@app.route('/api/shapes/<int:id>')
def api_shapes_id(id):

    shape = Shape.query.filter(Shape.id == id).first()

    if shape:
        if request.args.get('asGeoJSON'):
            return jsonify(shape.toGeoJSONDict())
        else:
            return jsonify(shape.toDict())
    else:
        return jsonify(error="Shape not found."), 404

# stops

@app.route('/api/stops')
def api_stops():

    stops = None

    bbox = request.args.get('bbox')
    if bbox:
        east, north, west, south = bbox.split(",")
        #stops = Stop.query.filter(
        #    Stop.lon.between(float(east),float(west)),
        #    Stop.lat.between(float(north), float(south)),
        #        ).limit(500)
        #TODO remove sql injection?
        bbox = "POLYGON(({} {}, {} {}, {} {}, {} {}, {} {}))".format(north, east, \
                north, west, south, west, south, east, north, east)
        app.logger.debug(bbox)
        stops = Stop.query.filter(Stop.geometry.intersects(bbox))
    else:
        stops = Stop.query.all()

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
    trips = None
    q = request.args.get('q')
    if q:
        trips = Trip.query.filter(or_(
            Trip.headsign.like("%" + q + "%"),
            Trip.short_name.like("%" + q + "%")
            )).all()
    else:
        trips = Trip.query.all()
    return jsonify(trips = toDictList(trips))

@app.route('/api/trips/<int:id>')
def api_trips_id(id):
    trip = Trip.query.filter(Trip.id == id).first()
    if trip:
        return jsonify(trip.toDict())
    else:
        return jsonify(error="Stop not found."), 404

# transfers

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

# routes

@app.route('/api/routes')
def api_routes():
    routes = None
    q = request.args.get('q')
    if q:
        routes = Route.query.filter(or_( \
            Route.short_name.like("%" + q + "%"),
            Route.long_name.like("%" + q + "%")
            )).all()
    else:
        routes = Route.query.all()
    return jsonify(routes = toDictList(routes))


@app.route('/api/routes/<int:id>')
def api_routes_id(id):
    route = Route.query.filter(Route.id == id).first()
    if route:
        return jsonify(route.toDict())
    else:
        return jsonify(error="Stop not found."), 404


@app.route('/api/routes/<int:id>/trips')
def api_route_id_trips(id):
    trips = Trip.query.filter(Trip.route_id == id).all()
    if trips:
        #return str(toDictList(trips))
        return jsonify(trips=toDictList(trips))
    else:
        return jsonify(error="Nothing found."), 404


@app.route('/api/trips/<int:trip_id>/stoptimes')
def api_route_id_stops(trip_id):
    stop_times = StopTime.query.filter(StopTime.trip_id == trip_id).all()
    if stop_times:
        return jsonify(stoptimes=toDictList(stop_times))
    else:
        return jsonify(error="Nothing found"), 404

@app.route('/api/trips/<int:trip_id>/stops')
def api_trips_id_stops(trip_id):
    stop_times = StopTime.query.filter(StopTime.trip_id == trip_id).all()
    stop_ids = [stop.stop_id for stop in stop_times]
    stops = Stop.query.filter(Stop.id.in_(stop_ids))
    if stops:
        return jsonify(stops=toDictList(stops))
    else:
        return jsonify(error="Nothing found"), 404

if __name__ == '__main__':
    app.run(debug=True)

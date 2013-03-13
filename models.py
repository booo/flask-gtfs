# -*- coding: utf-8 -*-
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

from geoalchemy import GeometryColumn, Point, WKTSpatialElement, Geometry

import os

app = Flask(__name__, instance_relative_config=True)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres:testing@localhost/postgres'
db = SQLAlchemy(app)

class Agency(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    url = db.Column(db.String(1024))
    timezone = db.Column(db.String(256))

    def __init__(self, id, name, url, timezone):
        self.id = id
        self.name = name
        self.url = url
        self.timezone = timezone

    def __repr__(self):
        return '<Agency %r>' % self.name

    def toDict(self):
        return {
                'id': self.id,
                'name': self.name,
                'url': self.url,
                'timezone': self.timezone
               }


class Stop(db.Model):

    id = db.Column(db.BigInteger, primary_key=True)
    code = db.Column(db.String(256))
    name = db.Column(db.String(256))
    desc = db.Column(db.String(256))
    geometry = GeometryColumn(Geometry())
    lat =  db.Column(db.Float)
    lon = db.Column(db.Float)
    type = db.Column(db.Integer)
    parent_station = db.Column(db.BigInteger)

    def __init__(self, id, code, name, desc, lat, lon, type, parent_station=None):
        self.id = id
        self.code = code
        self.name = name
        self.desc = desc
        self.geometry = WKTSpatialElement("POINT({} {})".format(lat, lon))
        self.lat = lat
        self.lon = lon
        self.type = type
        self.parent_station = parent_station

    def __repr__(self):
        return '<Stop %r>' % self.name

    def toDict(self):
        return {
                'id': self.id,
                'code': self.code,
                'name': self.name,
                'desc': self.desc,
                'lat': self.lat,
                'lon': self.lon,
                'type': self.type,
                'parent_station': self.parent_station
               }

    def toGeoJSONDict(self):
        return {
            'type': 'Feature',
            'id': self.id,
            'geometry': {
                'type': 'Point',
                'coordinates': [self.lon, self.lat]
                },
            'properties': {
                'code': self.code,
                'name': self.name,
                'desc': self.desc,
                'type': self.type,
                'parent_station': self.parent_station
                }
            }

class Route(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    agency_id = db.Column(db.Integer)
    short_name = db.Column(db.String(256))
    long_name = db.Column(db.String(256))
    type = db.Column(db.Integer)

    def __init__(self, id, agency_id, short_name, long_name, type):
        self.id = id
        self.agency_id = agency_id
        self.short_name = short_name
        self.long_name = long_name
        self.type = type

    def __repr__(self):
        return '<Route %r>' % self.short_name

    def toDict(self):
        return {
                'id': self.id,
                'agency_id': self.agency_id,
                'short_name': self.short_name,
                'long_name': self.long_name,
                'type': self.type
               }

class Trip(db.Model):

    route_id = db.Column(db.Integer)
    service_id = db.Column(db.Integer)
    id = db.Column(db.Integer, primary_key=True)
    headsign = db.Column(db.String(256))
    short_name = db.Column(db.String(256))
    direction_id = db.Column(db.Integer)
    block_id = db.Column(db.Integer)
    shape_id = db.Column(db.Integer)

    def __init__(self, route_id, service_id, id, headsign, short_name,
            direction_id, block_id, shape_id):
        self.route_id = route_id
        self.service_id = service_id
        self.id = id
        self.headsign = headsign;
        self.short_name = short_name
        self.direction_id = direction_id
        self.block_id = block_id
        self.shape_id = shape_id

    def __repr__(self):
        return '<Trip %r>' % self.short_name

    def toDict(self):
        return {
                'route_id': self.route_id,
                'service_id': self.service_id,
                'id': self.id,
                'headsign': self.headsign,
                'short_name': self.short_name,
                'direction_id': self.direction_id,
                'block_id': self.block_id,
                'shape_id': self.shape_id,
               }

class Transfer(db.Model):

    from_stop_id = db.Column(db.BigInteger, primary_key=True)
    to_stop_id = db.Column(db.BigInteger, primary_key=True)
    type = db.Column(db.Integer)
    min_transfer_time = db.Column(db.Integer) #in seconds?

    def __init__(self, from_stop_id, to_stop_id, type, min_transfer_time):
        self.from_stop_id = from_stop_id
        self.to_stop_id = to_stop_id
        self.type = type
        self.min_transfer_time = min_transfer_time

    def toDict(self):
        return {
                'from_stop_id': self.from_stop_id,
                'to_stop_id': self.to_stop_id,
                'type': self.type,
                'min_transfer_time': self.min_transfer_time
               }


class StopTime(db.Model):

    trip_id = db.Column(db.BigInteger, primary_key=True)
    arrival_time = db.Column(db.String(8))
    departure_time = db.Column(db.String(8))
    stop_id = db.Column(db.BigInteger, primary_key=True)
    stop_sequence = db.Column(db.Integer, primary_key=True)

    def __init__(self, trip_id, arrival_time, departure_time, stop_id, stop_sequence):
        self.trip_id = trip_id
        self.arrival_time = arrival_time
        self.departure_time = departure_time
        self.stop_id = stop_id
        self.stop_sequence = stop_sequence


class Shape(db.Model):

    id = db.Column(db.BigInteger, primary_key=True)
    geometry = GeometryColumn(Geometry())

    def __init__(self, id, geometry=None):
        self.id = id
        self.geometry = geometry

    def toDict(self):
        return { 'id': self.id }

    def toGeoJSONDict(self):
        return {
            'type': 'Feature',
            'id': self.id,
            'geometry': {
                'type': 'LineString',
                'coordinates': self.geometry.coords(db.session)
                },
            }


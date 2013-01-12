# -*- coding: utf-8 -*-
import csv
from datetime import datetime

from models import Agency, Stop, Route, Trip, StopTime, Transfer

import codecs, cStringIO

def stringToInt(s):
    if s != '':
        return int(s)
    else:
        return None

class UTF8Recorder:

    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)

    def __iter__(self):
        return self

    def next(self):
        return self.reader.next().encode("utf-8")

class UnicodeReader:

    def __init__(self, f):
        f = UTF8Recorder(f, 'utf-8')
        self.reader = csv.reader(f)

    def next(self):
        row = self.reader.next()
        return [unicode(s, "utf-8") for s in row]

    def __iter__(self):
        return self

class AgencyParser(object):

    def __init__(self, filename):
        self.filename = filename

    def parse(self):
        with open(self.filename, 'rb') as file:
            reader = UnicodeReader(file)
            #read the header
            columns = reader.next()
            for line in reader:
                id, name, url, timezone = line
                yield Agency(id, name, url, timezone)

class StopParser(object):

    def __init__(self, filename):
        self.filename = filename

    def parse(self):
        with open(self.filename, 'rb') as file:
            reader = UnicodeReader(file)
            #read the header
            columns = reader.next()
            for line in reader:
                id, code, name, desc, lat, lon, type, parent_station = \
                    line
                parent_station = stringToInt(parent_station)
                yield Stop(id, code, name, desc, lat, lon, type, parent_station)

class RouteParser(object):

    def __init__(self, filename):
        self.filename = filename

    def parse(self):
        with open(self.filename, 'rb') as file:
            reader = UnicodeReader(file)
            #read the header
            columns = reader.next()
            for line in reader:
                id, agency_id, short_name, long_name, type = line
                yield Route(id, agency_id, short_name, long_name, type)


class TripParser(object):

    def __init__(self, filename):
        self.filename = filename

    def parse(self):
        with open(self.filename, 'rb') as file:
            reader = UnicodeReader(file)
            #read the header
            columns = reader.next()
            for line in reader:
                route_id, service_id, id, headsign, short_name, direction_id, \
                block_id, shape_id = line
                direction_id = stringToInt(direction_id)
                block_id = stringToInt(block_id)
                shape_id = stringToInt(shape_id)
                yield Trip(route_id, service_id, id, headsign, short_name, \
                        direction_id, block_id, shape_id)

class TransferParser(object):

    def __init__(self, filename):
        self.filename = filename

    def parse(self):
        with open(self.filename, 'rb') as file:
            reader = UnicodeReader(file)
            #read the header
            columns = reader.next()
            for line in reader:
                from_stop_id, to_stop_id, type, min_transfer_time = \
                    line
                min_transfer_time = stringToInt(min_transfer_time)
                yield Transfer(from_stop_id, to_stop_id, type, \
                        min_transfer_time)

class StopTimeParser(object):

    def __init__(self, filename):
        self.filename = filename

    def parse(self):
        with open(self.filename, 'rb') as file:
            reader = UnicodeReader(file)
            #read the header
            columns = reader.next()
            for line in reader:
                trip_id, arrival_time, departure_time, stop_id, stop_sequence \
                        = line
                #arrival_time = datetime.strptime(arrival_time, \
                #        '%H:%M:%S').time()
                #departure_time = datetime.strptime(departure_time, \
                #        "%H:%M:%S").time()
                yield StopTime(trip_id, arrival_time, departure_time, stop_id, \
                        stop_sequence)

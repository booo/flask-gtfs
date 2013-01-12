from gtfsparser import AgencyParser, StopParser, RouteParser, TripParser, \
    TransferParser, StopTimeParser

from sqlalchemy.engine import Engine
from sqlalchemy import event

from models import db

from time import time

db.drop_all()
db.create_all()

start = time()
agencyParser = AgencyParser('./data/agency.txt')
for agency in agencyParser.parse():
    db.session.add(agency)
    db.session.commit()

print("Done with agencies after {} milliseconds.".format(time() - start))

start = time()
stopParser = StopParser('./data/stops.txt')
for stop in stopParser.parse():
    db.session.add(stop)
    db.session.commit()

print("Done with stops after {} milliseconds.".format(time() - start))

start = time()
routeParser = RouteParser('./data/routes.txt')
for route in routeParser.parse():
    db.session.add(route)
    db.session.commit()

print("Done with routes after {} milliseconds.".format(time() - start))

start = time()
tripParser = TripParser('./data/trips.txt')
for trip in tripParser.parse():
    db.session.add(trip)
    db.session.commit()

print("Done with trips after {} milliseconds.".format(time() - start))

start = time()
transferParser = TransferParser('./data/transfers.txt')
for transfer in transferParser.parse():
    db.session.add(transfer)
    db.session.commit()

print("Done with transfers after {} milliseconds.".format(time() - start))

#stopTimeParser = StopTimeParser('./data/stop_times.txt')
#for stopTime in stopTimeParser.parse():
#    db.session.add(stopTime)
#    db.session.commit()
#
#print("Done with stop times.")

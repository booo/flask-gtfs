from gtfsparser import AgencyParser, StopParser, RouteParser, TripParser, \
    TransferParser, StopTimeParser

from sqlalchemy.engine import Engine
from sqlalchemy import event

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA synchronous=OFF")
    cursor.close()

from models import db

db.drop_all()
db.create_all()

agencyParser = AgencyParser('./data/agency.txt')
for agency in agencyParser.parse():
    db.session.add(agency)
    db.session.commit()

print("Done with agencies.")

stopParser = StopParser('./data/stops.txt')
for stop in stopParser.parse():
    db.session.add(stop)
    db.session.commit()

print("Done with stops.")

routeParser = RouteParser('./data/routes.txt')
for route in routeParser.parse():
    db.session.add(route)
    db.session.commit()

print("Done with routes.")

tripParser = TripParser('./data/trips.txt')
for trip in tripParser.parse():
    db.session.add(trip)
    db.session.commit()

print("Done with trips.")

transferParser = TransferParser('./data/transfers.txt')
for transfer in transferParser.parse():
    db.session.add(transfer)
    db.session.commit()

print("Done with transfers.")

#stopTimeParser = StopTimeParser('./data/stop_times.txt')
#for stopTime in stopTimeParser.parse():
#    db.session.add(stopTime)
#    db.session.commit()
#
#print("Done with stop times.")

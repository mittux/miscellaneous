#!/usr/bin/python
import sqlite3
import datetime as dt
import Adafruit_DHT
import sys

_DBFILE = '/home/pi/training/my_raspberrypi/Adafruit_Python_DHT/examples/internalweather.db'
_SENSOR = Adafruit_DHT.AM2302
_PIN = 4


class parameters(object):
    def __init__(self):
        self.date_of_entry = None
        self.time_of_entry = None
        self.temperature = None
        self.humidity = None


def connect_db_create_table():
    global conn
    conn = sqlite3.connect(_DBFILE)
    conn.execute('''CREATE TABLE IF NOT EXISTS INTERNAL_WEATHER
      (id          integer primary key autoincrement not null,
       dateofentry text,
       timeofentry text,
       temperature real not null,
       humidity    real not null);''')


def insert_into_table(p):
    global conn
    str0 = "insert into INTERNAL_WEATHER (dateofentry,\
                                          timeofentry,\
                                          temperature,\
                                          humidity)\
                                          values("+"\""+str(p.date_of_entry)+"\","\
                                             +"\""+str(p.time_of_entry)+"\","\
                                             +str(p.temperature)+","\
                                             +"\""+str(p.humidity)+"\");";

    conn.execute(str0)
    conn.commit()


def get_internal_weather():
 
    p = parameters()
    dt_now = dt.datetime.now()
    p.date_of_entry = dt_now.date()
    p.time_of_entry = dt_now.strftime("%H:%M:%S")

    humidity, temperature = Adafruit_DHT.read_retry(_SENSOR, _PIN)

    if humidity is not None and temperature is not None:
        p.temperature = temperature
        p.humidity = humidity
    else:
        return None

    return p


def main():
    connect_db_create_table()
    w = get_internal_weather()
    if w:
        insert_into_table(w)
    conn.close()


if __name__ == "__main__":
    sys.exit(main())

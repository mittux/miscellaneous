#!/usr/bin/python3
"""
  This script is run as a cron job on the raspberrypi every hour
  It logs London weather data information using openweathermap API
"""
import requests
import sqlite3
import datetime as dt
import sys

try:
  from myopenweather import *
except ImportError:
  print("*** API Key not set! ***")

_LONDON_ID = '2643743'
_DBFILE = '/home/pi/programming/my_python/miscellaneous/weather/openweather.db'

class parameters(object):
    def __init__(self):
        self.date_of_entry = None
        self.time_of_entry = None
        self.temp_max = None
        self.temp_min = None
        self.temp_curr = None
        self.pressure = None
        self.humidity = None
        self.windspeed = None
        self.winddeg = None
        self.weather = None

def connect_db_create_table():
    global conn
    conn = sqlite3.connect(_DBFILE)
    conn.execute('''CREATE TABLE IF NOT EXISTS LDN_WEATHER
      (id          integer primary key autoincrement not null,
       dateofentry text,
       timeofentry text,
       tempmax     real not null,
       tempmin     real not null,
       temp        real not null,
       pressure    real not null,
       humidity    real not null,
       windspeed   real not null,
       winddeg     real not null,
       weather     text);''')

def insert_into_table(p):
    global conn
    str0 = "insert into LDN_WEATHER (dateofentry,\
                                     timeofentry,\
                                     tempmax,\
                                     tempmin,\
                                     temp,\
                                     pressure,\
                                     humidity,\
                                     windspeed,\
                                     winddeg,\
                                     weather)\
                                     values("+"\""+str(p.date_of_entry)+"\","\
                                             +"\""+str(p.time_of_entry)+"\","\
                                             +str(p.temp_max)+","\
                                             +str(p.temp_min)+","\
                                             +str(p.temp_curr)+","\
                                             +str(p.pressure)+","\
                                             +str(p.humidity)+","\
                                             +str(p.windspeed)+","\
                                             +str(p.winddeg)+","\
                                             +"\""+str(p.weather)+"\");";

    #print(str0)
    conn.execute(str0)
    conn.commit()

    
def get_weather_data():
    payload = {'id': _LONDON_ID, 'appid': API_KEY, 'units': 'metric' }
    r = requests.get("http://api.openweathermap.org/data/2.5/weather?", params=payload)

    r.raise_for_status()

    response = r.json()

    # print JSON response
    #print(response)

    # TODO: Abandoning timestamp from JSON as they are not unique
    #london = pytz.timezone('Europe/London')
    #import pytz
    #fmt = '%Y-%m-%d %H:%M:%S'
    #london_dt = london.localize(dt.datetime.utcfromtimestamp(int(response['dt'])))
    #print(london_t.strftime(fmt)

    p = parameters()
    # TODO: Check if tags exists in JSON before assigning
    dt_now = dt.datetime.now()
    p.date_of_entry = dt_now.date()
    p.time_of_entry = dt_now.strftime("%H:%M:%S")
    p.temp_max = response['main']['temp_max']
    p.temp_min = response['main']['temp_min']
    p.temp_curr = response['main']['temp']
    p.pressure = response['main']['pressure']
    p.humidity = response['main']['humidity']
    p.windspeed = response['wind']['speed']
    p.winddeg = response['wind']['deg']
    p.weather = response['weather'][0]['main']

    return p

def main():
    """Main entry for point"""
    connect_db_create_table()
    insert_into_table(get_weather_data())
    conn.close()

if __name__ == "__main__":
    sys.exit(main())

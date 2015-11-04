#!/usr/bin/python3
"""
  This script is run as a cron job on the raspberrypi every hour
  It logs London weather data information using openweathermap API
"""
import requests
import sqlite3
import datetime as dt
import sys
from threading import Thread

try:
  from myopenweather import *
except ImportError:
  print("*** API Key not set! ***")

citiesId = {
            'LONDON' : '2643743',
            'COCHIN' : '1273874',
            'NASHVILLE' : '4644585'
}

tableNames = { 
             'LONDON' : 'LDN',
             'COCHIN' : 'KOC',
             'NASHVILLE' : 'NAS'
}

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

def create_table(city):
    global conn
    conn.execute('CREATE TABLE IF NOT EXISTS '+tableNames[city]+'_WEATHER\n\
      (id          integer primary key autoincrement not null,\n\
       dateofentry text,\n\
       timeofentry text,\n\
       tempmax     real not null,\n\
       tempmin     real not null,\n\
       temp        real not null,\n\
       pressure    real not null,\n\
       humidity    real not null,\n\
       windspeed   real not null,\n\
       winddeg     real not null,\n\
       weather     text);')

def insert_into_table(p, city):
    global conn
    str0 = "insert into "+tableNames[city]+"_WEATHER (dateofentry,\
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

    
def get_weather_data(city):
    payload = {'id': citiesId[city], 'appid': API_KEY, 'units': 'metric' }
    r = requests.get("http://api.openweathermap.org/data/2.5/weather?", params=payload)

    r.raise_for_status()

    response = r.json()

    p = parameters()
    # JSON may not be well-formed, so check before assigning
    dt_now = dt.datetime.now()
    p.date_of_entry = dt_now.date()
    p.time_of_entry = dt_now.strftime("%H:%M:%S")
    if response.get('main'):
        if response['main'].get('temp_max'):
            p.temp_max = response['main']['temp_max']
        if response['main'].get('temp_min'):
            p.temp_min = response['main']['temp_min']
        if response['main'].get('temp'):
            p.temp_curr = response['main']['temp']
        if response['main'].get('pressure'):
            p.pressure = response['main']['pressure']
        if response['main'].get('humidity'):
            p.humidity = response['main']['humidity']
    if response.get('wind'):
        if response['wind'].get('speed'):
            p.windspeed = response['wind']['speed']
        if response['wind'].get('deg'):
            p.winddeg = response['wind']['deg']
    if response.get('weather'):
        if response['weather'][0]:
            if response['weather'][0].get('main'):
                p.weather = response['weather'][0]['main']

    return p

class GetWeatherThread(Thread):
    def __init__(self, city):
        super().__init__(name=city)
        self.data = None

    def run(self):
        self.data = get_weather_data(self.name)

def main():
    """Main entry for point"""

    global conn
    conn = sqlite3.connect(_DBFILE)

    threads = []

    # put weather data retrieval for different cities on separate threads
    for city in citiesId.keys():
        thread = GetWeatherThread(city)
        thread.start()
        threads.append(thread)

    # wait for threads to complete    
    for thread in threads:
        thread.join()

    for thread in threads:
        create_table(thread.name)
        insert_into_table(thread.data, thread.name)

    conn.close()

if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/python2
import requests
import datetime as dt
import sys
import time
import pickle
import paho.mqtt.client as mqtt
import max7219.led as led
from max7219.font import proportional, CP437_FONT

try:
  from myopenweather import API_KEY as weather_api_key
  from mynewsapi import API_KEY as news_api_key
except ImportError:
  print("*** API Key not set! ***")

_READING_ID = '2639577'
_CITY_ID = _READING_ID
_PUBLIC_BROKER = "iot.eclipse.org"
_TOPIC = "internal_weather"


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


def on_message(client, userdata, msg):
    global int_weather

    int_weather = pickle.loads(msg.payload)

    client.disconnect()
    return int_weather


def get_internal_weather():

    global int_weather

    client = mqtt.Client()
    client.connect(_PUBLIC_BROKER, 1883, 60)
    client.subscribe(_TOPIC)

    client.on_message = on_message

    client.loop_forever()

    return int_weather


def get_weather_data():
    '''get current weather information from openweathermap'''
    payload = {'id': _CITY_ID, 'appid': weather_api_key, 'units': 'metric' }

    try:
        r = requests.get("http://api.openweathermap.org/data/2.5/weather?", params=payload)
        response = r.json()
    except Exception as err:
        raise err

    if response is None:
        return None
    p = parameters()

    # JSON may not be well-formed, so check before assigning
    dt_now = dt.datetime.now()
    p.date_of_entry = dt_now.date()
    p.time_of_entry = dt_now.strftime("%2H:%2M:%2S")
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


def get_headlines():
    '''get top 5 headlines from guardian uk'''
    payload = { 'source' : 'the-guardian-uk',
                'sortBy' : 'top',
                'apiKey' : news_api_key  }

    try:
        r = requests.get("https://newsapi.org/v1/articles?", params=payload)
        response = r.json()
    except Exception as err:
        raise err

    if response is None:
        yield None

    dt_now = dt.datetime.now()
    time_now = dt_now.strftime("%2H:%2M")

    for s in response['articles'][:5]:
        headline = s['title']
        # fix unusual characters
        headline = headline.encode('ascii', 'xmlcharrefreplace')
        headline = headline.replace("&#8217;","'")
        yield headline


def display_on_led_matrix(text):
    global device
    device.show_message(text, font=proportional(CP437_FONT))


def main():
    global device
    device = led.matrix(2)
    device.orientation(270)

    try:
        w = get_weather_data()
        s = ''.join([str(w.time_of_entry[:5]),
                         ' Outside:',
                         ' %sC' % str(w.temp_curr),
                         ' %s' % str(w.humidity), '%',
                         ' %s' % str(w.weather),
                         ' %sm/s ' % str(w.windspeed)])
        display_on_led_matrix(s)

        w = get_internal_weather()
        t, h = '%.1f' % w[3], '%.1f' % w[4]
        s = ''.join([' Inside:',
                     ' %sC' % str(t),
                     ' %s' % str(h), '%'])
        display_on_led_matrix(s)
        time.sleep(0.8)

        for h in get_headlines():
            display_on_led_matrix(h)
            time.sleep(1)

    except Exception as err:
        print(err)
    finally:
        device.clear()


if __name__ == "__main__":
    sys.exit(main())

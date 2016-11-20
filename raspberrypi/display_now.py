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


class Parameters:
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


class InternalWeather:
    '''class that use MQTT to get the newest sensor reading'''
    _PUBLIC_BROKER = "iot.eclipse.org"
    _TOPIC = "internal_weather"
    _client = mqtt.Client()
    _weather_data = None

    def __init__(self):
        self._client.connect(self._PUBLIC_BROKER, 1883, 60)
        self._client.subscribe(self._TOPIC)
        self._client.on_message = self.on_message

    @property
    def weather_data(self):
        self._client.loop_forever()
        return self._weather_data

    @staticmethod
    def on_message(client, userdata, msg):
        InternalWeather._weather_data = pickle.loads(msg.payload)
        client.disconnect()

    @staticmethod
    def add_units(data):
        return str('%.1f' % data[3])+'C', str('%.1f' % data[4])+'%'


class ExternalWeather:
    '''class that gets current weather from openweathermap'''
    _READING_ID = '2639577'
    _CITY_ID = _READING_ID

    def __init__(self):
        self._payload = {'id': self._CITY_ID, 'appid': weather_api_key, 'units': 'metric' }
        self._weather_data = None

    def get_weather(self):
        try:
            r = requests.get("http://api.openweathermap.org/data/2.5/weather?", params=self._payload)
            response = r.json()
        except Exception as err:
            raise err

        if response is None:
            return None
        p = Parameters()

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

    @property
    def weather_data(self):
        self._weather_data = self.get_weather()
        return self._weather_data

    @staticmethod
    def add_units(data):
        '''return temperature, humidity and windspeed with appropriate units'''
        return str(data.temp_curr)+'C', str(data.humidity)+'%', str(data.windspeed)+'m/s'


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
        ew = ExternalWeather()
        we = ew.weather_data
        t, h, w = ew.add_units(we)
        s = ''.join([str(we.time_of_entry[:5]),' Outside:',' ',t,' ',h,' ',w,' ',we.weather])
        display_on_led_matrix(s)

        iw = InternalWeather()
        t, h = iw.add_units(iw.weather_data)
        s = ''.join([' Inside:',' ',t,' ',h])
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

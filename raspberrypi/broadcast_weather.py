#!/usr/bin/python
import sqlite3
import paho.mqtt.client as mqtt
import pickle
import sys

PUBLIC_BROKER = "iot.eclipse.org"
TOPIC = "internal_weather"
DB_FILE = '/home/pi/training/my_raspberrypi/Adafruit_Python_DHT/examples/internalweather.db'


def get_latest_weather():

    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    #find the newest entry
    cursor.execute("""SELECT * FROM INTERNAL_WEATHER ORDER BY ID DESC LIMIT 1;""")

    w = tuple(cursor.fetchone())

    return pickle.dumps(w)


def main():
    client = mqtt.Client()
    client.connect(PUBLIC_BROKER, 1883, 60)

    client.publish(TOPIC, get_latest_weather(), retain=True)
    client.disconnect()


if __name__ == "__main__":
    sys.exit(main())

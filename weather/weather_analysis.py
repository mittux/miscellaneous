import os
import sys
import sqlite3
import calendar
"""
  Does some basic analysis of london weather by querying the database
"""


def show_database_info():
    """
        shows basic database info
    """
    global conn
    global numberOfDays
    cursor = conn.cursor()

    # find the number of samples
    cursor.execute("""
    SELECT COUNT(*) AS samples FROM LDN_WEATHER;
    """)
    samplePoints = cursor.fetchone()['samples']
    print("There are %s data points in this database" % samplePoints)

    # find the
    cursor.execute("""
    SELECT COUNT(DISTINCT dateofentry) AS days FROM LDN_WEATHER;
    """)
    numberOfDays = cursor.fetchone()['days']
    print("There is weather data for %s days in this database" % numberOfDays)


def show_max_temperature_and_hottest_days():
    """
        shows the maximum temperature and the hottest days
    """
    global conn
    cursor = conn.cursor()

    # find maximum temperature
    cursor.execute("""
    SELECT MAX(tempmax) AS max FROM LDN_WEATHER;
    """)
    maxTemp = cursor.fetchone()['max']
    print("The maximum temperature was %s Celsius and it happened on " % maxTemp, end='')

    # find days with maximum temperature
    cursor.execute("""
    SELECT DISTINCT dateofentry FROM LDN_WEATHER WHERE tempmax IN (SELECT MAX(tempmax) FROM LDN_WEATHER);
    """)
    for row in cursor.fetchall():
        print(row['dateofentry'], end=' ')
    print()


def show_min_temperature_and_coldest_days():
    """
        shows the minimum temperature and the coldest days
    """
    global conn
    cursor = conn.cursor()

    # find minimum temperature
    cursor.execute("""
    SELECT MIN(tempmin) AS min FROM LDN_WEATHER;
    """)
    minTemp = cursor.fetchone()['min']
    print("The minimum temperature was %s Celsius and it happened on " % minTemp, end='')

    # find days with minimum temperature
    cursor.execute("""
    SELECT DISTINCT dateofentry FROM LDN_WEATHER WHERE tempmin IN (SELECT MIN(tempmin) FROM LDN_WEATHER);
    """)
    for row in cursor.fetchall():
        print(row['dateofentry'], end=' ')
    print()


def show_weather_types():
    """
        shows the different types of weather recorded
    """
    global conn
    cursor = conn.cursor()

    # find weather types
    cursor.execute("""
    SELECT DISTINCT weather FROM LDN_WEATHER;
    """)

    print("The different weather types seen are:")
    for row in cursor.fetchall():
        print(' ', row['weather'])


def show_dominant_weather_type():
    """
        shows the dominant weather type
    """
    global conn
    cursor = conn.cursor()

    # find the weather type and the number of days of each
    cursor.execute("""
    SELECT  weather, COUNT(weather) AS count FROM LDN_WEATHER GROUP BY weather ORDER BY count DESC;
    """)

    row = cursor.fetchone()
    print("The most dominant weather type was '%s'" % row['weather'])


def show_average_temperature():
    """
        shows the average temperature
    """
    global conn
    global avgTemp
    cursor = conn.cursor()

    # finds the average temperature
    cursor.execute("""
    SELECT  ROUND(AVG(temp),2) AS average FROM LDN_WEATHER;
    """)

    avgTemp = float(cursor.fetchone()['average'])
    print("The average temperature was %s Celsius" % avgTemp)


def show_days_above_average():
    """
        shows the days which had daily average above the average in this period
    """
    global conn
    global avgTemp
    cursor = conn.cursor()

    # finds daily averages for all days
    cursor.execute("""
    SELECT  SUBSTR(dateofentry,1,4) AS year,
            SUBSTR(dateofentry,6,2) AS month,
            SUBSTR(dateofentry,9,2) AS day,
            ROUND(AVG(temp),2) as daily_avg
    FROM LDN_WEATHER GROUP BY dateofentry;
    """)

    print("The following days had daily average temperatures above average:")
    for row in cursor.fetchall():
        if float(row['daily_avg']) > avgTemp:
            print(' ', row['day'], calendar.month_name[int(row['month'])], row['year'])


def main():
    db_filename = "openweather.db"
    fullFile = os.path.abspath(db_filename)

    if not os.path.exists(db_filename):
        print('{} not found !!!'.format(db_filename))
        return 1

    global conn
    global numberOfDays

    with sqlite3.connect(db_filename) as conn:
        conn.row_factory = sqlite3.Row

        print("\nRandom information from this database:")
        show_database_info()
        show_max_temperature_and_hottest_days()
        show_min_temperature_and_coldest_days()
        show_weather_types()
        show_dominant_weather_type()
        show_average_temperature()
        show_days_above_average()
        # TODO - show_most_humid_days()
        # TODO - show_most_windy_days()

if __name__ == "__main__":
    sys.exit(main())

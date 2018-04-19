import geojson
import csv
from pprint import *
"""
    TBD
"""

def get_airports_data():
    with open('airports.csv', mode='r') as infile:
        reader = csv.reader(infile)
        mydict = []
        i = 0
        for row in reader:
            if i == 0:
                k0, k1, k2, k3, k4, k5, k6, k7, k8, k9, k10, k11, k12, k13 = row
                i = 1
            else:
                mydict.append({k0:row[0], k1:row[1], k2:row[2], k3:row[3], k4:row[4], k5:row[5], k6:row[6],
                               k7:row[7], k8:row[8], k9:row[9], k10:row[10], k11:row[11], k12:row[12], k13:row[13]})
            
        return mydict

def create_map(df):
    """
       Returns a GeoJSON file that can be rendered on gist.github.com
    """

    # Define type of GeoJSON we're creating
    geo_map = {"type": "FeatureCollection"}

    item_list = []

    for each in df:

        X = each['Longitude'].strip()
        Y = each['Latitude'].strip()

        # Skip any zero coordinates
        if X == 0 or Y == 0 or X == "" or Y == "":
            continue

        data = {}

        # Assigne line items to appropriate GeoJSON fields.
        data['type'] = 'Feature'
        data['id'] = str(each['Airport ID'])
        data['properties'] = {'Name': each['Name'],
                              'Country': each['Country'],
                              'IATA': each['IATA'] if each['IATA'] != "\\N" else '-'}
        data['geometry'] = {'type': 'Point',
                            'coordinates': (float(X), float(Y))}

        item_list.append(data)

    # For each point in our item_list, we add the point to our
    # dictionary.  setdefault creates a key called 'features' that
    # has a value type of an empty list.  With each iteration, we
    # are appending our point to that list.
    for point in item_list:
        geo_map.setdefault('features', []).append(point)

    with open('airports.geojson', 'w') as f:
       f.write(geojson.dumps(geo_map))

def main():
    cdata = get_airports_data()
    create_map(cdata)

if __name__ == "__main__":
    main()
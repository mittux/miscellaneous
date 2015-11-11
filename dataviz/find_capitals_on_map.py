import wbdata
import pandas as pd
import geojson
from pprint import *
"""
    This program extracts all countries using World Bank API
    It then generates a GeoJSON file of all the capital cities
    This file can be viewed on http://geojson.io/#map=2/20.0/0.0
"""

def get_capitals_data():

    # Getting country data from worldbank.org
    countries_df = pd.DataFrame(wbdata.get_country())

    # filtering out only countries with capitals
    countries_with_capitals = countries_df[countries_df["capitalCity"] != '']

    return countries_with_capitals

def create_map(df):
    """
       Returns a GeoJSON file that can be rendered on gist.github.com
    """

    # Define type of GeoJSON we're creating
    geo_map = {"type": "FeatureCollection"}

    item_list = []

    for each in df.iterrows():

        X = each[1]['longitude'].strip()
        Y = each[1]['latitude'].strip()

        # Skip any zero coordinates
        if X == 0 or Y == 0 or X == "" or Y == "":
            continue

        data = {}

        # Assigne line items to appropriate GeoJSON fields.
        data['type'] = 'Feature'
        data['id'] = str(each[0])
        data['properties'] = {'capital': each[1]['capitalCity'],
                              'country': each[1]['name']}
        data['geometry'] = {'type': 'Point',
                            'coordinates': (float(X), float(Y))}

        item_list.append(data)

    # For each point in our item_list, we add the point to our
    # dictionary.  setdefault creates a key called 'features' that
    # has a value type of an empty list.  With each iteration, we
    # are appending our point to that list.
    for point in item_list:
        geo_map.setdefault('features', []).append(point)

    with open('capitals.geojson', 'w') as f:
       f.write(geojson.dumps(geo_map))

def main():
    cdata = get_capitals_data()
    return create_map(cdata)

if __name__ == "__main__":
    main()
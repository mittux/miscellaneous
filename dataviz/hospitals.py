import requests
import geojson
from itertools import count
from pprint import pprint


def get_hospitals():

	try:
		r = requests.get("https://data.gov.uk/data/api/service/health/hospitals/all_hospitals?", params={})
		r.raise_for_status()
		response = r.json()
	except Exception as err:
		print(err)


	hospitals = { i:(e['name'], e['city'], e['county'], e['longitude'], e['latitude']) 
                                          for i,e in zip(count(1), response['result']) }	

	return hospitals


def create_map(hospitals):
    """
       Returns a GeoJSON file that can be rendered on gist.github.com
    """

    # Define type of GeoJSON we're creating
    geo_map = {"type": "FeatureCollection"}

    item_list = []

    for each in hospitals.values():

        X = each[3].strip()
        Y = each[4].strip()

        # Skip any zero coordinates
        if X == 0 or Y == 0 or X == "" or Y == "":
            continue

        data = {}

        # Assign line items to appropriate GeoJSON fields.
        data['type'] = 'Feature'
        data['id'] = each[0]
        data['properties'] = {'Name': each[0], 'City': each[1], 'County': each[2]}
        data['geometry'] = {'type': 'Point',
                            'coordinates': (float(X), float(Y))}

        item_list.append(data)

    # For each point in our item_list, we add the point to our
    # dictionary.  setdefault creates a key called 'features' that
    # has a value type of an empty list.  With each iteration, we
    # are appending our point to that list.
    for point in item_list:
        geo_map.setdefault('features', []).append(point)

    with open('hospitals.geojson', 'w') as f:
       f.write(geojson.dumps(geo_map))


def main():
    return create_map(get_hospitals())


if __name__ == "__main__":
    main()




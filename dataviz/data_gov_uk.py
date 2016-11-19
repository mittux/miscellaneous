import requests
import geojson
from itertools import count
from pprint import pprint


services = {
#    service name : (url path, query string)    
    'hospitals' : ('health/hospitals/all_hospitals?', {}),
    'railways'  : ('transport/sql?', { 'query': 'select * from naptan_railway_stations' }),
    'coaches'   : ('transport/sql?', { 'query': 'select * from naptan_coach_stations' }),
    'ferries'   : ('transport/sql?', { 'query': 'select * from naptan_ferry_ports' }),
}


def get_json_response(name):
    '''get json from data gov'''

    url_path, query_dict = services[name][:2]

    try:
        r = requests.get(''.join(['https://data.gov.uk/data/api/service/', url_path]), params=query_dict)
        r.raise_for_status()
        response = r.json()
    except Exception as err:
        print(err)

    return response['result']


def extract_info(name):
    '''extraction depends on json payload'''

    response = get_json_response(name)

    if name=='hospitals':
        return ((e['longitude'], e['latitude'], e['name'], e['city'], e['county']) for e in response)        

    if name=='railways':
        return ((e['latlong']['coordinates'][0], e['latlong']['coordinates'][1], e['stationname']) for e in response)

    if name=='coaches':
        return ((e['latlong']['coordinates'][0], e['latlong']['coordinates'][1], e['name']) for e in response)

    if name=='ferries':
        return ((e['latlong']['coordinates'][0], e['latlong']['coordinates'][1], e['name']) for e in response)


def create_map(name, iterator):
    """
       Returns a GeoJSON file that can be rendered on gist.github.com
    """

    # Define type of GeoJSON we're creating
    geo_map = {"type": "FeatureCollection"}

    item_list = []

    for each in iterator:

        X = each[0]
        Y = each[1]

        # Skip any zero coordinates
        if X == 0 or Y == 0 or X == "" or Y == "":
            continue

        data = {}

        # Assign line items to appropriate GeoJSON fields.
        data['type'] = 'Feature'
        data['id'] = each[0]
        if name=='hospitals':
            data['properties'] = {'Name': each[2], 'City': each[3], 'County': each[4]}
        else:
            data['properties'] = {'Name': each[2]}

        data['geometry'] = {'type': 'Point',
                            'coordinates': (float(X), float(Y))}

        item_list.append(data)

    # For each point in our item_list, we add the point to our
    # dictionary.  setdefault creates a key called 'features' that
    # has a value type of an empty list.  With each iteration, we
    # are appending our point to that list.
    for point in item_list:
        geo_map.setdefault('features', []).append(point)

    with open(name+'.geojson', 'w') as f:
       f.write(geojson.dumps(geo_map))


def main():
    for name in services:
        info = extract_info(name)
        create_map(name, info)


if __name__ == "__main__":
    main()

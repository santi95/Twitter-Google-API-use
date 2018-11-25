from CiudadesGet import main
import requests
import json
import time
from collections import namedtuple
from config import key1


def get_coordenadas(ciudad, key1=key1):
    # Maps API KEY
    GOOGLE_MAPS_API_URL = 'https://maps.googleapis.com/maps/api/geocode/json?'
    coor = namedtuple('Coordenadas', 'Ciudad, Lat, Lon')
    j = ciudad
    params = "address={}".format(j)
    url = GOOGLE_MAPS_API_URL + params + '&key=' + key1
    req = requests.get(url)
    res = req.json()
    if res['results'] == []:
        return None
    result = res['results'][0]
    lat = result['geometry']['location']['lat']
    lon = result['geometry']['location']['lng']
    ntupla = coor(ciudad, lat, lon)
    return ntupla

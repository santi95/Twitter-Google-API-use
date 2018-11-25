import CoordenadasGet
import requests
from requests_oauthlib import OAuth1
import pickle
import urllib3
from datetime import datetime, timedelta
from collections import namedtuple
from config import API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET

# lista_coor = CoordenadasGet.get_coordinates()


url = 'https://api.twitter.com/1.1/account/verify_credentials.json'
auth = OAuth1(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
requests.get(url, auth=auth)
id_lugares = []
hastags_lugar = {}


# Con la interfaz le preguntamos el lugar,
# bucamos sus coordenadas,
# sacamos el id del lugar
# Buscamos los trending topics
# Sacamos los 5 mas populares

def datos_twitter(coordenadas):
    lat = coordenadas.Lat
    lon = coordenadas.Lon

    req = 'https://api.twitter.com/1.1/trends/closest.json?lat={lat}&long={long}'.format(
        lat=lat, long=lon)
    r = requests.get(req, auth=auth)
    tweets = r.json()[0]

    id_lugar = tweets['woeid']
    # Hacemos el segundo request, de los populares
    req2 = 'https://api.twitter.com/1.1/trends/place.json?id={}'.format(
        id_lugar)
    r2 = requests.get(req2, auth=auth)
    hashtags_populares = r2.json()[0]
    hashtags_populares = hashtags_populares['trends']
    lista_tuplas_a_ordenar = []

    for i in hashtags_populares:
        if i['tweet_volume'] != None:
            lista_tuplas_a_ordenar.append((i['name'], i['tweet_volume']))
        else:
            lista_tuplas_a_ordenar.append((i['name'], 0))

    lista_tuplas_a_ordenar.sort(key=lambda x: int(x[1]))
    lista_tuplas_a_ordenar.reverse()
    # Top 5 Trending Topics
    trending = lista_tuplas_a_ordenar[:5]
    return trending


def get_twiteros(coordenadas):
    desde = datetime.today() - timedelta(days=5)
    # EL desde está malo, cambia el since
    req = 'https://api.twitter.com/1.1/search/tweets.json?since{year}-{month}-{day}&geocode={lat},{long},3mi&count=20'.format(
        year=desde.year, month=desde.month, day=desde.day, lat=coordenadas.Lat,
        long=coordenadas.Lon)
    a = requests.get(req, auth=auth)
    person = namedtuple('Person', 'followers usuario tweet')
    usuarios = []
    for i in range(20):
        try:
            base = a.json()['statuses'][i]
            usuarios.append(person(base['user']['followers_count'],
                                   base['user']['screen_name'], base['text']))
            # Get numero seguidores, hacerles display
        except:
            print('No habían 20 tweets ahí')
    return usuarios

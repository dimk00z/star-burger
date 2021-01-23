import requests
from geopy.distance import distance


def fetch_coordinates(apikey, place):
    base_url = 'https://geocode-maps.yandex.ru/1.x'
    params = {'geocode': place, 'apikey': apikey, 'format': 'json'}
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    places_found = response.json(
    )['response']['GeoObjectCollection']['featureMember']
    most_relevant = places_found[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(' ')

    return lon, lat


def get_distance(apikey, first_place, second_place):
    try:
        first_coords = fetch_coordinates(apikey, first_place)
        second_coords = fetch_coordinates(apikey, second_place)
    except IndexError:
        return None

    result_distance = distance(first_coords, second_coords)

    return result_distance

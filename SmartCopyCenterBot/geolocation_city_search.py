from dadata import Dadata
from config import DA_TOKEN


dadata = Dadata(DA_TOKEN)


def geoloc_city_search(lat, lon):
    result = dadata.geolocate(name="address", lat=lat, lon=lon)
    for kek in result:
        tmp = kek.get('data')
        city = tmp['city']
    return city


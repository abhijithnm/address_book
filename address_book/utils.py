import geocoder

from math import sin, cos, sqrt, atan2, radians


def get_user_coordinates():
    """This function is to find user's current coordinate"""
    user_coordinate = geocoder.ip('me')
    return user_coordinate.latlng[0], user_coordinate.latlng[1]


def find_distance(lat, lon, lat2, lon2):
    """This funtion is to find distance from the given coordinates"""

    # Approximate radius of earth in km
    R = 6373.0

    lat1= radians(lat)
    lon1= radians(lon)

    dlon = radians(lon2) - lon1
    dlat = radians(lat2) - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance
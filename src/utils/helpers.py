import requests
from utils.config_loader import load_yaml



def geocode_location(name):
    """
    Geocode a location name to get its latitude and longitude using the Nominatim API.

    Parameters:
    -----------------
        name (str): The name of the bar to geocode.
    
    Returns:
    -----------------
        tuple: A tuple containing the latitude and longitude of the location.
    """

    url = load_yaml("settings")["location"]["location_url"]
    params = {
        'q': name,
        'format': 'json',
        'limit': 1
    }

    response = requests.get(url, params=params)
    data = response.json()

    if data:
        latitude = float(data[0]['lat'])
        longitude = float(data[0]['lon'])
        return latitude, longitude
    else:
        raise ValueError(f"Could not geocode location: {name}")
    

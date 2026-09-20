'''
weather ingestion module for NightPulse Intelligence.

Author : Andrew Francey
Description : This module contains functions to fetch weather data from the OpenWeatherMap API.
Created : 2026-09-15

Import as : import weather_api
'''

## Import necessary libraries
## --------------------------------
import os
import requests
import datetime

from utils.config_loader import load_yaml

## Core API client
## -----------------------------------------

class WeatherAPIClient:
    '''
    A client for fetching weather data from the selected weather API.
    '''

    settings = load_yaml("settings")["weather_api"]
    credentials = load_yaml("credentials")["weather_api"]

    def __init__(self):
        self.api_key = self.credentials["api_key"]
        self.base_url = self.settings["base_url"]
        self.provider = self.settings["provider"]
        self.units = self.settings["units"]

    def _request(self, params: dict[str, any]) -> dict[str, any]:
        '''
        Internal method to make a request to the weather API.

        Parameters:
        -----------------
            params (dict): A dictionary of parameters to send with the request.
        
        Returns:
        -----------------
            dict: The JSON response from the API as a dictionary.
        '''
        params['appid'] = self.api_key
        response = requests.get(self.base_url, params=params)

        if response.status_code != 200:
            raise RuntimeError(
                f"Error fetching weather data: {response.status_code} - {response.text}"
            )

        return response.json()

    ## Public methods
    ## -----------------------------------------

    def get_current(self, lat: float, lon: float) -> dict[str, any]:
        '''
        Fetch the current weather data for a given latitude and longitude.

        Parameters:
        -----------------
            lat (float): Latitude of the location.
            lon (float): Longitude of the location.
        
        Returns:
        -----------------
            dict: The current weather data as a dictionary.
        '''
        params = {
            'lat': lat,
            'lon': lon,
            'units': self.units,
            'exclude': 'minutely,hourly,daily,alerts'
        }

        return self._request(params)

    def get_hourly(self, lat: float, lon: float) -> dict[str, any]:
        '''
        Fetch the hourly weather forecast for a given latitude and longitude.

        Parameters:
        -----------------
            lat (float): Latitude of the location.
            lon (float): Longitude of the location.
        
        Returns:
        -----------------
            dict: The hourly weather forecast data as a dictionary.
        '''
        params = {
            'lat': lat,
            'lon': lon,
            'units': self.units,
            'exclude': 'current,minutely,daily,alerts'
        }

        return self._request(params)

    def get_daily(self, lat: float, lon: float) -> dict[str, any]:
        '''
        Fetch the daily weather forecast for a given latitude and longitude.

        Parameters:
        -----------------
            lat (float): Latitude of the location.
            lon (float): Longitude of the location.
        
        Returns:
        -----------------
            dict: The daily weather forecast data as a dictionary.
        '''
        params = {
            'lat': lat,
            'lon': lon,
            'units': self.units,
            'exclude': 'current,minutely,hourly,alerts'
        }

        return self._request(params)

    def get_historical(self, lat: float, lon: float, dt: datetime.datetime) -> dict[str, any]:
        '''
        Fetch historical weather data for a given latitude, longitude, and datetime.

        Parameters:
        -----------------
            lat (float): Latitude of the location.
            lon (float): Longitude of the location.
            dt (datetime): The datetime for which to fetch historical data.
        
        Returns:
        -----------------
            dict: The historical weather data as a dictionary.
        '''
        params = {
            'lat': lat,
            'lon': lon,
            'dt': int(dt.timestamp()),
            'units': self.units
        }

        return self._request(params)

## Normalization layer
## -----------------------------------------

def normalize_current(raw: dict[str, any]) -> dict[str, any]:
    '''
    Normalize the raw current weather data into a structured ML-ready format.

    Parameters:
    -----------------
        raw (dict): The raw current weather data from the API.
    
    Returns:
    -----------------
        dict: The normalized current weather data.
    '''

    current = raw.get("current", {})
    return {
        "timestamp": current.get("dt"),
        "temperature": current.get("temp"),
        "feels_like": current.get("feels_like"),
        "pressure": current.get("pressure"),
        "humidity": current.get("humidity"),
        "dew_point": current.get("dew_point"),
        "uvi": current.get("uvi"),
        "clouds": current.get("clouds"),
        "visibility": current.get("visibility"),
        "wind_speed": current.get("wind_speed"),
        "wind_deg": current.get("wind_deg"),
        "weather_main": current.get("weather", [{}])[0].get("main"),
        "weather_description": current.get("weather", [{}])[0].get("description")
    }

def normalize_hourly(raw: dict[str, any]) -> list:
    '''
    Normalize the raw hourly weather data into a structured ML-ready format.

    Parameters:
    -----------------
        raw (dict): The raw hourly weather data from the API.
    
    Returns:
    -----------------
        list: A list of normalized hourly weather data dictionaries.
    '''

    hourly_data = raw.get("hourly", [])
    normalized = []

    for hour in hourly_data:
        normalized.append({
            "timestamp": hour.get("dt"),
            "temperature": hour.get("temp"),
            "feels_like": hour.get("feels_like"),
            "pressure": hour.get("pressure"),
            "humidity": hour.get("humidity"),
            "dew_point": hour.get("dew_point"),
            "rain": hour.get("rain", {}).get("1h"),
            "uvi": hour.get("uvi"),
            "clouds": hour.get("clouds"),
            "snow": hour.get("snow", {}).get("1h"),
            "visibility": hour.get("visibility"),
            "wind_speed": hour.get("wind_speed"),
            "wind_deg": hour.get("wind_deg"),
            "weather_main": hour.get("weather", [{}])[0].get("main"),
            "weather_description": hour.get("weather", [{}])[0].get("description")
        })

    return normalized

def normalize_daily(raw: dict[str, any]) -> list:
    '''
    Normalize the raw daily weather data into a structured ML-ready format.

    Parameters:
    -----------------
        raw (dict): The raw daily weather data from the API.
    
    Returns:
    -----------------
        list: A list of normalized daily weather data dictionaries.
    '''

    daily_data = raw.get("daily", [])
    normalized = []

    for day in daily_data:
        normalized.append({
            "timestamp": day.get("dt"),
            "temp_day": day.get("temp", {}).get("day"),
            "temp_min": day.get("temp", {}).get("min"),
            "temp_max": day.get("temp", {}).get("max"),
            "feels_like_day": day.get("feels_like", {}).get("day"),
            "feels_like_night": day.get("feels_like", {}).get("night"),
            "feels_like_eve": day.get("feels_like", {}).get("eve"),
            "feels_like_morn": day.get("feels_like", {}).get("morn"),
            "pressure": day.get("pressure"),
            "humidity": day.get("humidity"),
            "dew_point": day.get("dew_point"),
            "rain": day.get("rain"),
            "uvi": day.get("uvi"),
            "snow": day.get("snow"),
            "clouds": day.get("clouds"),
            "wind_speed": day.get("wind_speed"),
            "wind_deg": day.get("wind_deg"),
            "weather_main": day.get("weather", [{}])[0].get("main"),
            "weather_description": day.get("weather", [{}])[0].get("description")
        })

    return normalized


## Convenience wrapper for ingestion pipeline
## -------------------------------------------

def fetch_weather_bundle(lat: float, lon: float) -> dict[str, any]:
    '''
    Fetch a complete weather data bundle (current, hourly, daily) for a given latitude and longitude.

    Parameters:
    -----------------
        lat (float): Latitude of the location.
        lon (float): Longitude of the location.
    
    Returns:
    -----------------
        dict: A dictionary containing normalized current, hourly, and daily weather data.
    '''

    client = WeatherAPIClient()

    raw_current = client.get_current(lat, lon)
    raw_hourly = client.get_hourly(lat, lon)
    raw_daily = client.get_daily(lat, lon)

    return {
        "current": normalize_current(raw_current),
        "hourly": normalize_hourly(raw_hourly),
        "daily": normalize_daily(raw_daily)
    }

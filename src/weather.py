import requests
import json
import os

class WeatherAPI(object):
    def __init__(self):
        self.url = os.environ.get("WEATHER_URL") 
    
    def request_location(self, city_name, location_type, country_code):
        """
            Requests a location from weather company location services
            API. Useful for retrieving the latitude and longitude of a
            place.
        """
        request_suffix = "/api/weather/v3/location/search?"
        params = { 'query': city_name, 'locationType': location_type, 'countryCode': country_code, 'language': "en-US" }
 
        location_request = requests.get(self.url + request_suffix, params=params)
        
        return location_request.status_code, json.loads(location_request.content)

    def request_weather(self, latitude, longitude):
        """
            Given a latitude and longitude, gets the weather at that
            location
        """

        request_suffix = "/api/weather/v1/geocode/{0}/{1}/observations.json".format(latitude, longitude)
        params = { 'language' : "en-US", 'units': "m" }

        print request_suffix

        weather_request = requests.get(self.url + request_suffix, params=params)

        return weather_request.status_code, json.loads(weather_request.content)

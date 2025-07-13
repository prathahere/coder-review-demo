import requests
import time
import json

class WeatherFetcher:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "http://api.weatherapi.com/v1/current.json"
        self.cache = {}

    def fetch_weather(self, city):
        if city in self.cache:
            return self.cache[city]

        params = {
            "key": self.api_key,
            "q": city
        }

        response = requests.get(self.base_url, params=params)
        data = response.json()  # ❌ No status code check

        self.cache[city] = data  # ⚠️ Caches raw response, even if error
        return data

    def display_weather(self, data):
        print(f"Weather for: {data['location']['name']}")
        print(f"Temperature: {data['current']['temp_c']}°C")
        print(f"Condition: {data['current']['condition']['text']}")
        print(f"Wind Speed: {data['current']['wind_kph']} kph")

    def save_to_file(self, data, city):
        path = f"data/{c

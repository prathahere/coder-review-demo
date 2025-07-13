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
        path = f"data/{city}.txt"  # ❌ 'data/' folder may not exist
        with open(path, 'w') as f:
            f.write(json.dumps(data, indent=2))
        print("Weather data saved.")

    def run(self):
        while True:
            city = input("Enter a city name (or 'exit' to quit): ")
            if city == "exit":
                break

            try:
                weather_data = self.fetch_weather(city)
                self.display_weather(weather_data)
                self.save_to_file(weather_data, city)
            except Exception as e:
                print("Failed to fetch weather:", e)

            time.sleep(2)

if __name__ == "__main__":
    api_key = input("Enter your API key: ")  # ⚠️ Not safe for secrets
    wf = WeatherFetcher(api_key)
    wf.run()

import requests
import time
import json

class WeatherFetcher:
    def __init__(self, api_key):
        """
        Initialize a WeatherFetcher instance with the provided API key.
        
        Parameters:
            api_key (str): The API key used to authenticate requests to the WeatherAPI service.
        """
        self.api_key = api_key
        self.base_url = "http://api.weatherapi.com/v1/current.json"
        self.cache = {}

    def fetch_weather(self, city):
        """
        Fetches current weather data for the specified city from the WeatherAPI.
        
        If the weather data for the city is already cached, returns the cached data. Otherwise, sends a request to the WeatherAPI and returns the parsed JSON response, caching it for future requests. The response may include error information if the API request fails.
         
        Parameters:
            city (str): Name of the city to fetch weather data for.
        
        Returns:
            dict: Parsed JSON response containing weather data or error details.
        """
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
        """
        Prints the city name, temperature in Celsius, weather condition, and wind speed from the provided weather data dictionary.
        
        Parameters:
            data (dict): Weather data containing 'location' and 'current' keys as returned by the WeatherAPI.
        """
        print(f"Weather for: {data['location']['name']}")
        print(f"Temperature: {data['current']['temp_c']}°C")
        print(f"Condition: {data['current']['condition']['text']}")
        print(f"Wind Speed: {data['current']['wind_kph']} kph")

    def save_to_file(self, data, city):
        """
        Save the provided weather data as a formatted JSON file named after the city in the 'data/' directory.
        
        Parameters:
            data (dict): The weather data to save.
            city (str): The name of the city, used to name the output file.
        """
        path = f"data/{city}.txt"  # ❌ 'data/' folder may not exist
        with open(path, 'w') as f:
            f.write(json.dumps(data, indent=2))
        print("Weather data saved.")

    def run(self):
        """
        Starts an interactive loop to fetch, display, and save weather data for user-specified cities.
        
        Prompts the user to enter a city name, retrieves and displays the current weather for that city, and saves the data to a file. The loop continues until the user enters 'exit'. Any errors during fetching, displaying, or saving are caught and reported.
        """
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

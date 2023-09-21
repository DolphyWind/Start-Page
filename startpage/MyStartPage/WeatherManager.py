import geocoder
import requests

class WeatherManager:

    def __init__(self, latitude=None, longtitude=None):
        self.latitude, self.longtitude = latitude, longtitude

        self.weather_api_url: str = f"https://api.open-meteo.com/v1/forecast?latitude={self.latitude}&longitude={self.longtitude}&current_weather=true"

        self.is_day: bool = True
        self.temperature = 0
        self.weather_code = -1
        self.weather_classname = "wu-unknown"
        self.day_night_classname = "wu-day"

        self.fetch_weather_data()

    def fetch_weather_data(self):
        try:
            req = requests.get(self.weather_api_url)
        except:
            return

        if not str(req.status_code).startswith('2'):
            return

        weather_data: dict = req.json()
        current_weather = weather_data["current_weather"]
        self.is_day = current_weather["is_day"]
        self.temperature = current_weather["temperature"]
        self.weather_code = current_weather["weathercode"]
        self.day_night_classname = 'wu-day' if self.is_day else 'wu-night'

        if self.weather_code in (0, 1):
            self.weather_classname = 'wu-clear'
        elif self.weather_code == 2:
            self.weather_classname = 'wu-partlycloudy'
        elif self.weather_code == 3:
            self.weather_classname = 'wu-cloudy'
        elif self.weather_code in (45, 48):
            self.weather_classname = 'wu-fog'
        elif self.weather_code in (51, 53, 55, 56, 57, 61, 63, 65, 66, 67, 80, 81, 82):
            self.weather_classname = 'wu-rain'
        elif self.weather_code in (71, 73, 75, 77, 85, 86):
            self.weather_classname = 'wu-snow'
        elif self.weather_code in (95, 96, 99):
            self.weather_classname = 'wu-tstorms'



from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
import getpass
import geocoder
import requests
import json
from enum import Enum

class WeatherStatus(Enum):
    CLEAR = 0
    PARTLY_CLOUDY = 1
    CLOUDY = 2
    FOGGY = 3
    RAINY = 4
    SNOWY = 5
    THUNDERSTORM = 6
    UNKNOWN = 7
    

"""
{'latitude': 41.0625, 'longitude': 28.9375, 'generationtime_ms': 0.2720355987548828, 'utc_offset_seconds': 0, 'timezone': 'GMT',
'timezone_abbreviation': 'GMT', 'elevation': 4.0,
'current_weather': {'temperature': 1.4, 'windspeed': 27.4, 'winddirection': 357.0, 'weathercode': 71, 'time': '2023-02-05T22:00'}}
"""

# Create your views here.
def get_weather_stats():
    g = geocoder.ip('me')
    lat, lon = g.latlng
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    try:
        req = requests.get(url)
    except:
        pass
    if req.status_code == 200:
        data = req.json()
        temperature = data['current_weather']['temperature']
        weather_code = data['current_weather']['weathercode']
        weather_status = None
        if weather_code in (0, 1):
            weather_status = WeatherStatus.CLEAR
        elif weather_code == 2:
            weather_status = WeatherStatus.PARTLY_CLOUDY
        elif weather_code == 3:
            weather_status = WeatherStatus.CLOUDY
        elif weather_code in (45, 48):
            weather_status = WeatherStatus.FOGGY
        elif weather_code in (51, 53, 55, 56, 57, 61, 63, 65, 66, 67, 80, 81, 82):
            weather_status = WeatherStatus.RAINY
        elif weather_code in (71, 73, 75, 77, 85, 86):
            weather_status = WeatherStatus.SNOWY
        elif weather_code in (95, 96, 99):
            weather_status = WeatherStatus.THUNDERSTORM
        else:
            weather_status = WeatherStatus.UNKNOWN
        
        return temperature, weather_status
        
    else:
        return None

def load_page(request):
    context_data = dict()
    context_data['name'] = getpass.getuser()
    print(get_weather_stats())
    
    return render(request, 'mainpage.html', context_data)
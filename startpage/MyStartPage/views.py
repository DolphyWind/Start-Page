from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
import getpass
from .SettingsManager import SettingsManager
from .DatetimeManager import DatetimeManager
from .WeatherManager import WeatherManager

def load_page(request):
    settings_filename = "settings.json"
    default_settings = {
        "name": getpass.getuser(),
        "search_engines": {
            "Google": "https://www.google.com/search?q=%s",
            "DuckDuckGo": "https://duckduckgo.com/?t=ffab&q=%s",
            "StartPage": "https://www.startpage.com/do/dsearch?query=%s",
        },
        "default_search_engine": "google"
    }

    settings_manager = SettingsManager(settings_filename, default_settings)
    datetime_manager = DatetimeManager()
    weather_manager = WeatherManager()

    # Settings
    username = settings_manager["name"]
    search_engine_name = settings_manager["default_search_engine"]
    search_url = settings_manager["search_engines"][search_engine_name]

    # Datetime data
    datetime_string = datetime_manager.get_datetime_string()
    part_of_the_day = datetime_manager.get_part_of_the_day()

    # Weather data
    day_night_classname = weather_manager.day_night_classname
    temperature = weather_manager.temperature
    weather_classname = weather_manager.weather_classname

    # CONTEXT DATA SETUP
    context_data = dict()
    context_data['name'] = username
    context_data["search_engine_name"] = search_engine_name
    context_data['search_url'] = search_url

    context_data['datetime_string'] = datetime_string
    context_data['part_of_day'] = part_of_the_day

    context_data['day_night_classname'] = day_night_classname
    context_data['temperature'] = temperature
    context_data['weather_classname'] = weather_classname

    settings_manager.save_settings()  # Temporary
    return render(request, 'mainpage.html', context_data)
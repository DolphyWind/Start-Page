from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
from .Globals import globals

# Called automatically when user leaves the website
def save_settings(request):
    globals.settings_manager.save_settings()
    return HttpResponse(200, "Save Successfull!")

def load_page(request):
    globals.fetch()
    settings_manager = globals.settings_manager
    datetime_manager = globals.datetime_manager
    weather_manager = globals.weather_manager
    currency_manager = globals.currency_manager

    # Settings
    username = settings_manager["name"]
    search_engine_name = settings_manager["current_search_engine"]
    search_url = settings_manager["search_engines"][search_engine_name]

    # Datetime data
    datetime_string = datetime_manager.datetime_string
    part_of_the_day = datetime_manager.part_of_the_day
    clock_initial = datetime_manager.clock_initial

    # Weather data
    day_night_classname = weather_manager.day_night_classname
    temperature = weather_manager.temperature
    weather_classname = weather_manager.weather_classname

    # Currencies
    currency_list = currency_manager.fetch_multiple_currencies(settings_manager["currencies"])

    # CONTEXT DATA SETUP
    context_data = dict()
    context_data['name'] = username
    context_data["search_engine_name"] = search_engine_name
    context_data['search_url'] = search_url

    context_data['datetime_string'] = datetime_string
    context_data['part_of_day'] = part_of_the_day
    context_data['clock_initial'] = clock_initial

    context_data['day_night_classname'] = day_night_classname
    context_data['temperature'] = temperature
    context_data['weather_classname'] = weather_classname

    context_data['currency_list'] = currency_list
    context_data['categories'] = settings_manager["categories"]

    return render(request, 'mainpage.html', context_data)
import getpass
from .SettingsManager import SettingsManager
from .DatetimeManager import DatetimeManager
from .WeatherManager import WeatherManager
from .SettingsPresenceManager import SPM_File
from .CurrencyManager import CurrencyManager
import geocoder

class Globals:
    def __init__(self):
        self.settings_manager: SettingsManager = None
        self.datetime_manager: DatetimeManager = None
        self.weather_manager: WeatherManager = None
        self.currency_manager: CurrencyManager = None
        self.fetch()

    def fetch(self):
        settings_filename = "settings.json"
        latitude = 0
        longitude = 0

        try:
            latitude, longitude = geocoder.ip("me").latlng
        except:
            pass

        default_settings = {
            "name": getpass.getuser(),
            "latitude": latitude,
            "longitude": longitude,
            "search_engines": {
                "Google": "https://www.google.com/search?q=%s",
            },
            "current_search_engine": "Google",
            "currencies": [],
            "categories": []
        }

        self.settings_manager = SettingsManager(settings_presence_manager=SPM_File(settings_filename, default_settings))
        self.datetime_manager = DatetimeManager()
        self.weather_manager = WeatherManager(self.settings_manager.get_setting("latitude"), self.settings_manager.get_setting("longitude"))
        self.currency_manager = CurrencyManager()

    def get_context_data(self):
        # Settings
        username = self.settings_manager["name"]
        latitude = self.settings_manager["latitude"]
        longitude = self.settings_manager["longitude"]

        # Search engine settings
        search_engines = self.settings_manager["search_engines"]
        search_engine_name = self.settings_manager["current_search_engine"]

        search_url = ''
        if search_engine_name:
            search_url = search_engines[search_engine_name]

        # Datetime data
        datetime_string = self.datetime_manager.datetime_string
        part_of_the_day = self.datetime_manager.part_of_the_day
        clock_initial = self.datetime_manager.clock_initial

        # Weather data
        day_night_classname = self.weather_manager.day_night_classname
        temperature = self.weather_manager.temperature
        weather_classname = self.weather_manager.weather_classname

        # Currencies
        currencies = self.settings_manager["currencies"]
        currency_list = self.currency_manager.fetch_multiple_currencies(currencies)

        # Categories
        categories = self.settings_manager["categories"]

        # CONTEXT DATA SETUP

        context_data = dict()
        context_data['name'] = username
        context_data['latitude'] = latitude
        context_data['longitude'] = longitude
        context_data['search_engines'] = search_engines
        context_data["search_engine_name"] = search_engine_name
        context_data['search_url'] = search_url

        context_data['datetime_string'] = datetime_string
        context_data['part_of_day'] = part_of_the_day
        context_data['clock_initial'] = clock_initial

        context_data['day_night_classname'] = day_night_classname
        context_data['temperature'] = temperature
        context_data['weather_classname'] = weather_classname

        context_data['currencies'] = currencies
        context_data['currency_list'] = currency_list
        context_data['categories'] = categories

        return context_data

globals = Globals()

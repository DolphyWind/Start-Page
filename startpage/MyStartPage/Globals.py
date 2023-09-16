import getpass
from .SettingsManager import SettingsManager
from .DatetimeManager import DatetimeManager
from .WeatherManager import WeatherManager
from .SettingsPresenceManager import SPM_File
from .CurrencyManager import CurrencyManager

class Globals:
    def __init__(self):
        self.settings_manager = None
        self.datetime_manager = None
        self.weather_manager = None
        self.currency_manager = None
        self.fetch()

    def fetch(self):
        settings_filename = "settings.json"
        default_settings = {
            "name": getpass.getuser(),
            "search_engines": {
                "Google": "https://www.google.com/search?q=%s",
                "DuckDuckGo": "https://duckduckgo.com/?t=ffab&q=%s",
                "StartPage": "https://www.startpage.com/do/dsearch?query=%s",
            },
            "current_search_engine": "Google",
            "currencies": [
                {"USD": "TRY"},
                {"EUR": "TRY"},
            ],
            "categories": []
        }

        self.settings_manager = SettingsManager(settings_presence_manager=SPM_File(settings_filename, default_settings))
        self.datetime_manager = DatetimeManager()
        self.weather_manager = WeatherManager()
        self.currency_manager = CurrencyManager()


globals = Globals()

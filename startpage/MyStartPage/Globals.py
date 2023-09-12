import getpass
from .SettingsManager import SettingsManager
from .DatetimeManager import DatetimeManager
from .WeatherManager import WeatherManager

class Globals:
    def __init__(self):
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

        self.settings_manager = SettingsManager(settings_filename, default_settings)
        self.datetime_manager = DatetimeManager()
        self.weather_manager = WeatherManager()


globals = Globals()

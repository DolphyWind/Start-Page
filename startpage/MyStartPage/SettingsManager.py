import json

class SettingsManager:
    def __init__(self, filename: str, defaultSettings: dict):
        self.filename: str = filename
        self.__settings: dict = {}
        self.__default_settings: dict = defaultSettings

        self.load_settings()

    def load_settings(self) -> None:
        try:
            with open(self.filename, "r") as file:
                self.__settings = json.load(file)
        except FileNotFoundError:
            self.__settings = self.__default_settings
            self.save_settings()

    def save_settings(self) -> None:
        with open(self.filename, "w") as f:
            json.dump(self.__settings, f)
    def get_setting(self, settingName: str):
        if settingName in self.__settings:
            return self.__settings[settingName]

        self.__settings[settingName] = self.get_default_setting(settingName)
        return self.__settings[settingName]

    def get_default_setting(self, settingName: str):
        if not self.does_setting_exists(settingName):
            raise RuntimeError("Setting does not exists!")
        return self.__default_settings[settingName]

    def set_setting(self, settingName: str, value):
        if not self.does_setting_exists(settingName):
            raise RuntimeError("Setting does not exists!")
        self.__settings[settingName] = value

    def does_setting_exists(self, settingName: str) -> bool:
        return settingName in self.__default_settings

    def __getitem__(self, item):
        return self.get_setting(item)

    def __setitem__(self, key, value):
        return self.set_setting(key, value)

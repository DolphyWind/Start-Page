import json
from .SettingsPresenceManager import ISettingsPresenceManager

class SettingsManager:
    def __init__(self, settings_presence_manager: ISettingsPresenceManager):
        self.__settings_presence_manager = settings_presence_manager
        self.__settings: dict = {}
        self.__default_settings: dict = settings_presence_manager.default_settings

        self.load_settings()

    def load_settings(self) -> None:
        self.__settings = self.settings_presence_manager.load_settings()

    def save_settings(self) -> None:
        self.settings_presence_manager.save_settings(self.settings)

    def get_setting(self, settingName: str):
        if settingName in self.settings:
            return self.settings[settingName]

        self.settings[settingName] = self.get_default_setting(settingName)
        return self.settings[settingName]

    def get_default_setting(self, settingName: str):
        if not self.does_setting_exists(settingName):
            raise RuntimeError("Setting does not exists!")
        return self.default_settings[settingName]

    def set_setting(self, settingName: str, value):
        if not self.does_setting_exists(settingName):
            raise RuntimeError("Setting does not exists!")
        self.__settings[settingName] = value

    def does_setting_exists(self, settingName: str) -> bool:
        return settingName in self.default_settings

    def __getitem__(self, item):
        return self.get_setting(item)

    def __setitem__(self, key, value):
        return self.set_setting(key, value)

    def reset_settings(self) -> None:
        self.__settings = self.__default_settings

    @property
    def settings(self) -> dict:
        return self.__settings

    @property
    def default_settings(self) -> dict:
        return self.settings_presence_manager.default_settings

    @property
    def settings_presence_manager(self):
        return self.__settings_presence_manager

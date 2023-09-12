from abc import ABC, abstractmethod
import json

class ISettingsPresenceManager(ABC):
    """
    Capable of loading and saving settings. It is an abstract base class so the classes that derive from this class should do all the work
    """

    def __init__(self, default_settings: dict):
        self.__default_settings = default_settings

    @property
    def default_settings(self) -> dict:
        return self.__default_settings

    @abstractmethod
    def load_settings(self) -> dict:
        pass

    @abstractmethod
    def save_settings(self, settings: dict) -> None:
        pass


# SPM stands for Settings Presence Manager
class SPM_File(ISettingsPresenceManager):

    def __init__(self, filename: str, default_settings: dict):
        super().__init__(default_settings)
        self.__filename = filename

    def load_settings(self) -> dict:
        try:
            with open(self.filename, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            def_settings = self.default_settings
            self.save_settings(def_settings)
            return def_settings

    def save_settings(self, settings: dict) -> None:
        for key in self.default_settings.keys():
            if key not in settings.keys():
                settings[key] = self.default_settings[key]

        with open(self.filename, "w") as f:
            json.dump(settings, f)

    @property
    def filename(self):
        return self.__filename

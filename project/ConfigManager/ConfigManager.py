import configparser

from project.utils import CONSTANTS


class ConfigManager:
    """Basic settings settable from the settings menu"""

    __instance = None

    @staticmethod
    def get_instance():
        """Static access method."""
        if ConfigManager.__instance is None:
            ConfigManager()
        return ConfigManager.__instance

    def __init__(self):
        if ConfigManager.__instance is not None:
            raise Exception("This class is a singleton. Please use get_instance().")

        ConfigManager.__instance = self
        self._config = configparser.ConfigParser()
        self._config.read(CONSTANTS['CONFIG_FILE_LOCATION'])
        print(self._config)
        if not self._config.has_section('settings'):
            self._init_config()

    def _init_config(self):
        """Populates the config block with some default values."""
        self._config.add_section('settings')
        self._config.set('settings', 'persist_clipboard', 'true')
        self._config.set('settings', 'delete_after_paste', 'true')
        self._config.set('settings', 'auto_load_top', 'true')
        self.save()

    @property
    def persist_clipboard(self):
        return self._config.getboolean('settings', "persist_clipboard")

    @persist_clipboard.setter
    def persist_clipboard(self, value: bool):
        self._config['settings']["persist_clipboard"] = 'true' if value else 'false'

    @property
    def delete_after_paste(self):
        return self._config.getboolean('settings', "delete_after_paste")

    @delete_after_paste.setter
    def delete_after_paste(self, value: bool):
        self._config['settings']["delete_after_paste"] = 'true' if value else 'false'

    @property
    def auto_load_top(self):
        return self._config.getboolean('settings', "auto_load_top")

    @auto_load_top.setter
    def auto_load_top(self, value: bool):
        self._config['settings']["auto_load_top"] = 'true' if value else 'false'

    def save(self):
        with open(CONSTANTS['CONFIG_FILE_LOCATION'], 'w') as file:
            self._config.write(file)

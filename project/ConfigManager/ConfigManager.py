import configparser
import json

from project.utils import CONSTANTS


class ConfigManager:
    """Basic settings settable from the settings menu"""

    __instance = None

    @staticmethod
    def get_instance():
        """Singleton access method."""
        if ConfigManager.__instance is None:
            ConfigManager()
        return ConfigManager.__instance

    def __init__(self):
        if ConfigManager.__instance is not None:
            raise Exception("This class is a singleton. Please use get_instance().")

        ConfigManager.__instance = self
        self._config = configparser.ConfigParser()
        self._config.read(CONSTANTS['CONFIG_FILE_LOCATION'])
        if not self._config.has_section('settings'):
            self._init_config()

    def _init_config(self):
        """Populates the config block with some default values."""
        self._config.add_section('settings')
        self._config.add_section('plugin_settings')

        self._config.set('settings', 'persist_clipboard', 'true')
        # self._config.set('settings', 'delete_after_paste', 'true')
        self._config.set('settings', 'auto_load_top', 'true')

        self._config.set('plugin_settings', 'chain_all_plugins', 'false')
        self._config.set('plugin_settings', 'disabled_text_plugins', json.dumps([]))
        self._config.set('plugin_settings', 'disabled_image_plugins', json.dumps([]))

        self.save()

    @property
    def persist_clipboard(self):
        return self._config.getboolean('settings', "persist_clipboard")

    @persist_clipboard.setter
    def persist_clipboard(self, value: bool):
        self._config['settings']["persist_clipboard"] = 'true' if value else 'false'

    # @property
    # def delete_after_paste(self):
    #     return self._config.getboolean('settings', "delete_after_paste")
    #
    # @delete_after_paste.setter
    # def delete_after_paste(self, value: bool):
    #     self._config['settings']["delete_after_paste"] = 'true' if value else 'false'

    @property
    def auto_load_top(self):
        return self._config.getboolean('settings', "auto_load_top")

    @auto_load_top.setter
    def auto_load_top(self, value: bool):
        self._config['settings']["auto_load_top"] = 'true' if value else 'false'

    @property
    def chain_all_plugins(self):
        return self._config.getboolean('plugin_settings', 'chain_all_plugins')

    @chain_all_plugins.setter
    def chain_all_plugins(self, value: bool):
        self._config['plugin_settings']['chain_all_plugins'] = 'true' if value else 'false'

    @property
    def disabled_text_plugins(self):
        return json.loads(self._config.get('plugin_settings', 'disabled_text_plugins'))

    @disabled_text_plugins.setter
    def disabled_text_plugins(self, plugin_names: [str]):
        self._config['plugin_settings']['disabled_text_plugins'] = json.dumps(plugin_names)

    def disable_text_plugin(self, text_plugin_name: str):
        if text_plugin_name not in self.disabled_text_plugins:
            self.disabled_text_plugins = self.disabled_text_plugins + [text_plugin_name]

    def enable_text_plugin(self, text_plugin_name):
        _temp = self.disabled_text_plugins
        if text_plugin_name in _temp:
            _temp.remove(text_plugin_name)
            self.disabled_text_plugins = _temp

    @property
    def disabled_image_plugins(self):
        return json.loads(self._config.get('plugin_settings', 'disabled_image_plugins'))

    @disabled_image_plugins.setter
    def disabled_image_plugins(self, plugin_names: [str]):
        self._config['plugin_settings']['disabled_image_plugins'] = json.dumps(plugin_names)

    def disable_image_plugin(self, image_plugin_name: str):
        if image_plugin_name not in self.disabled_text_plugins:
            self.disabled_image_plugins = self.disabled_image_plugins + [image_plugin_name]

    def enable_image_plugin(self, image_plugin_name):
        _temp = self.disabled_image_plugins
        if image_plugin_name in _temp:
            _temp.remove(image_plugin_name)
            self.disabled_image_plugins = _temp

    def save(self):
        with open(CONSTANTS['CONFIG_FILE_LOCATION'], 'w') as file:
            self._config.write(file)

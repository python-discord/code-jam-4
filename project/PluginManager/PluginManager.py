import logging
import random

from PyQt5.QtGui import QPixmap

# from project.ConfigManager import ConfigManager
from project.Plugins import SpellingMistakesPlugin
from project.Plugins.SynonymPlugin import SynonymPlugin
from project.Stack import Stack


class PluginManager:

    def __init__(self):
        self._logger = logging.getLogger(self.__class__.__qualname__)
        self._text_plugins = []
        self._image_plugins = []

        self._disabled_plugin_names = set()

        # If this were a real application, would use importlib to dynamically import plugins
        # within this folder.
        self._text_plugins.append(SpellingMistakesPlugin())
        self._text_plugins.append(SynonymPlugin())

    def on_copy_text(self, text_input: str, stack: Stack):
        # _config = ConfigManager.get_instance()

        _plugin = random.choice(list(filter(lambda plugin: plugin.__class__.name()
                                            not in self._disabled_plugin_names,
                                            self._text_plugins)))

        self._logger.info("Passing " + text_input + " to plugins!")
        self._logger.info("Randomly chose plugin " + _plugin.__class__.__qualname__)
        _plugin.on_copy(text_input, stack)

    def on_paste_image(self, image_input: QPixmap, stack: Stack):
        pass

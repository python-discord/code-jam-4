import logging
import random

from PyQt5.QtGui import QPixmap

from project.ClipboardManager.ClipboardObject import TextClipboardObject, ImageClipboardObject
from project.ConfigManager import ConfigManager
from project.Plugins import SpellingMistakesPlugin
from project.Plugins.ImageRotatePlugin import ImageRotatePlugin
from project.Plugins.QuotePlugin import QuotePlugin
from project.Plugins.SynonymPlugin import SynonymPlugin
from project.Stack import Stack


class PluginManager:
    __instance = None

    @staticmethod
    def get_instance():
        """Static access method."""
        if PluginManager.__instance is None:
            PluginManager()
        return PluginManager.__instance

    def __init__(self):
        if PluginManager.__instance is not None:
            raise Exception("This class is a singleton. Please use get_instance().")

        PluginManager.__instance = self
        self._logger = logging.getLogger(self.__class__.__qualname__)
        self.text_plugins = []
        self.image_plugins = []

        self._config = ConfigManager.get_instance()

        # If this were a real application, would use importlib to dynamically import plugins
        # within this folder.
        self.text_plugins.append(SpellingMistakesPlugin())
        self.text_plugins.append(SynonymPlugin())
        self.text_plugins.append(QuotePlugin())

        self.image_plugins.append(ImageRotatePlugin())

    def on_copy_text(self, text_input: str, stack: Stack):
        """Function that is called by the ClipboardManager upon text copy"""

        _enabled_plugins = list(
            filter(lambda plugin: plugin.__class__.name() not in self._config.disabled_text_plugins,
                   self.text_plugins))

        if not _enabled_plugins:
            stack.push_item(TextClipboardObject(text_input))
            return

        _plugin = random.choice(list(_enabled_plugins))

        self._logger.info("Passing " + text_input + " to plugins!")
        self._logger.info("Randomly chose plugin " + _plugin.__class__.__qualname__)
        _plugin.on_copy(text_input, stack)

    def on_copy_image(self, image_input: QPixmap, stack: Stack):
        """Function that is called by the ClipboardManager upon image copy"""

        _enabled_plugins = list(
            filter(lambda plugin: plugin.__class__.name()not in self._config.disabled_image_plugins,
                   self.image_plugins))

        if not _enabled_plugins:
            stack.push_item(ImageClipboardObject(image_input))
            return

        _plugin = random.choice(_enabled_plugins)

        _plugin.on_copy(image_input, stack)

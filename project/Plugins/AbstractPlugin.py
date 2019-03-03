import logging
from abc import ABCMeta, abstractmethod
from enum import Enum

from project import Stack


class PluginTypes(Enum):
    TEXT = 'text'
    IMAGE = 'image'


class AbstractPlugin(metaclass=ABCMeta):
    """A plugin defines an operation to manipulate the item of a clipboard in some way."""

    def __init__(self):
        self._logger = logging.getLogger(self.__class__.name())

    @staticmethod
    def name() -> str:
        pass

    @staticmethod
    def description() -> str:
        pass

    @abstractmethod
    def onload(self):
        pass

    @staticmethod
    def getType(self) -> PluginTypes:
        pass

    @abstractmethod
    def unload(self):
        pass

    @abstractmethod
    def on_copy(self, copied_input: any, stack: Stack):
        """Applies the function upon the input,
        return value should be the same type as the input"""
        pass

    @abstractmethod
    def on_paste(self, stack: Stack):
        """Manipulates the stack in some way; able to get the currently selected item"""
        pass

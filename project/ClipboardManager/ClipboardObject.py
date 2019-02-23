from abc import ABCMeta
import datetime


class ClipboardObject(metaclass=ABCMeta):

    def __init__(self):
        self._date = datetime.datetime.now()

    def date(self):
        """Returns when this object was copied to clipboard"""
        return self._date


class TextClipboardObject(ClipboardObject):

    def __init__(self, text):
        super().__init__()
        self.text = text

    def set_text(self, text: str):
        self.text = text

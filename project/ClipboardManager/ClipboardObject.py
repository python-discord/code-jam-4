from abc import ABCMeta
import datetime

from PyQt5.QtGui import QPixmap


class ClipboardObject(metaclass=ABCMeta):

    def __init__(self):
        self._date = datetime.datetime.now()

    def date(self):
        """Returns when this object was copied to clipboard"""
        return self._date


class TextClipboardObject(ClipboardObject):

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.text == other.text
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __init__(self, text):
        super().__init__()
        self.text = text

    def set_text(self, text: str):
        self.text = text

    def __str__(self):
        return self.text

    def __repr__(self):
        return self.__str__()


class ImageClipboardObject(ClipboardObject):

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.pixmap.toImage() == other.pixmap.toImage()
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __init__(self, pixmap: QPixmap):
        super().__init__()
        self.pixmap = pixmap

    def getImage(self):
        return self.pixmap

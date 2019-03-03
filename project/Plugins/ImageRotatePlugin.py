# from PyQt5.QtGui import QPixmap
import random

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QTransform

from project import Stack
# from project.ClipboardManager.ClipboardObject import TextClipboardObject
from project.ClipboardManager.ClipboardObject import ImageClipboardObject
from project.Plugins import AbstractPlugin


def _rotate_pixmap(pixmap: QPixmap):
    """Helper function to rotate image in random multiples of 90 deg"""

    _transforms = [QTransform().rotate(0),
                   QTransform().rotate(90),
                   QTransform().rotate(180),
                   QTransform().rotate(270)]

    # pick a random transform
    _transform = random.choice(_transforms)
    return pixmap.transformed(_transform, Qt.SmoothTransformation)


class ImageRotatePlugin(AbstractPlugin):

    @staticmethod
    def name() -> str:
        return "ImageRotate"

    @staticmethod
    def description() -> str:
        return "Rotates your images so you have new ways of looking at them."

    def onload(self):
        pass

    def unload(self):
        pass

    def on_copy(self, copied_input: any, stack: Stack):
        stack.push_item(ImageClipboardObject(_rotate_pixmap(copied_input)))

    def on_paste(self, stack: Stack):
        return stack

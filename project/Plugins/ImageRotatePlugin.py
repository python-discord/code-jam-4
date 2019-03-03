# from PyQt5.QtGui import QPixmap

from project import Stack
# from project.ClipboardManager.ClipboardObject import TextClipboardObject
from project.Plugins import AbstractPlugin


# def _rotate_pixmap(pixmap: QPixmap):


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
        pass

    def on_paste(self, stack: Stack):
        return stack

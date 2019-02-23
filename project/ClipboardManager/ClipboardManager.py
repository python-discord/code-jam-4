"""Class encapsulating clipboard events"""
from PyQt5.Qt import QApplication, QClipboard  # noqa: F401
from project.Stack import Stack


def _clipboard_changed():
    print("Current Text", QApplication.clipboard().text())
    print("Current Image Info", QApplication.clipboard().pixmap())


class ClipboardManager:

    def __init__(self):
        QApplication.clipboard().dataChanged.connect(_clipboard_changed)
        self._clipboard_stack = Stack()

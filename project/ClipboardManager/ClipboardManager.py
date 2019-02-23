"""Class encapsulating clipboard events"""
from PyQt5.Qt import QApplication, QClipboard  # noqa: F401

from project.ClipboardManager.ClipboardObject import TextClipboardObject
from project.Stack import Stack


class ClipboardManager:

    def __init__(self):
        self._clipboard_state_callback = None
        QApplication.clipboard().dataChanged.connect(self._clipboard_changed)
        self._clipboard_stack = Stack()

    def _clipboard_changed(self):
        current_text = QApplication.clipboard().text()
        print("Current Text", QApplication.clipboard().text())
        print("Current Image Info", QApplication.clipboard().pixmap())

        if current_text and not (isinstance(self._clipboard_stack.peek(), TextClipboardObject)
                                 and self._clipboard_stack.peek().text == current_text):
            self._clipboard_stack.push_item(TextClipboardObject(current_text))

        if self._clipboard_state_callback is not None:
            self._clipboard_state_callback(self._clipboard_stack)

    # TODO: use Qt signals properly
    # https://stackoverflow.com/questions/36434706/pyqt-proper-use-of-emit-and-pyqtsignal
    def bind_clipboard_state_callback(self, function):
        self._clipboard_state_callback = function

"""Class encapsulating clipboard events"""
from PyQt5.Qt import QApplication, QClipboard  # noqa: F401
from PyQt5.QtCore import pyqtSignal, QObject, pyqtSlot

from project.ClipboardManager.ClipboardObject import TextClipboardObject
from project.Stack import Stack

# import logging


# https://stackoverflow.com/questions/36522809/
# pyqt5-connection-doesnt-work-item-cannot-be-converted-to-pyqt5-qtcore-qobject
class ClipboardManager(QObject):
    clipboard_changed_signal = pyqtSignal(Stack)

    def __init__(self):
        super().__init__()
        self._clipboard_state_callback = None
        QApplication.clipboard().dataChanged.connect(self._clipboard_changed)
        self.clipboard_stack = Stack()

    @pyqtSlot()
    def _clipboard_changed(self):
        current_text = QApplication.clipboard().text()
        print("Current Text", QApplication.clipboard().text())
        print("Current Image Info", QApplication.clipboard().pixmap())

        if current_text and not (isinstance(self.clipboard_stack.peek(), TextClipboardObject)
                                 and self.clipboard_stack.peek().text == current_text):
            self.clipboard_stack.push_item(TextClipboardObject(current_text))
            self.clipboard_changed_signal.emit(self.clipboard_stack)

        # if self._clipboard_state_callback is not None:
        #     self._clipboard_state_callback(self._clipboard_stack)

    # DONE: use Qt signals properly
    # https://stackoverflow.com/questions/36434706/pyqt-proper-use-of-emit-and-pyqtsignal
    # def bind_clipboard_state_callback(self, function):
    #     self._clipboard_state_callback = function

    def set_selected_object(self, idx):
        if not 0 <= idx < self.clipboard_stack.items_count():
            raise Exception("Index is out of bounds")

        """Highlights a particular row in the main window"""
        self.clipboard_stack.set_current_item(idx)

    def remove_clipboard_item(self):
        """Public function to remove a clipboard item"""
        self._remove_clipboard_item(self.clipboard_stack.current_item())
        self.clipboard_changed_signal.emit(self.clipboard_stack)

    def _remove_clipboard_item(self, idx):
        """Helper function to remove a item from the stack"""
        if not self.clipboard_stack.items_count():
            return

        if not 0 <= idx < self.clipboard_stack.items_count():
            raise Exception("Index is out of bounds")

        self.clipboard_stack.pop(idx)
        self.clipboard_changed_signal.emit(self.clipboard_stack)

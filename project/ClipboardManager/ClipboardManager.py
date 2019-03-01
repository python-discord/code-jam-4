"""Class encapsulating clipboard events"""
from PyQt5.Qt import QApplication, QClipboard  # noqa: F401
from PyQt5.QtCore import pyqtSignal, QObject, pyqtSlot

from project.ClipboardManager.ClipboardObject import TextClipboardObject, ImageClipboardObject
from project.Stack import Stack


# from project.Plugins.Text import Text

# import logging


# https://stackoverflow.com/questions/36522809/
# pyqt5-connection-doesnt-work-item-cannot-be-converted-to-pyqt5-qtcore-qobject
class ClipboardManager(QObject):
    clipboard_changed_signal = pyqtSignal(Stack)
    stack_changed_signal = pyqtSignal(Stack)

    def __init__(self):
        super().__init__()
        self._clipboard_state_callback = None
        self._last_text = None
        self._last_image = None

        QApplication.clipboard().dataChanged.connect(self._clipboard_changed)
        self.clipboard_stack = Stack()
        self.stack_changed_signal.connect(self._stack_changed)

    @pyqtSlot(Stack)
    def _stack_changed(self):
        """Slot to be called when the state of the stack changes (usually on add, move, delete, or moving items
        around """
        # copy the top of the stack into the clipboard if the stack is not empty.
        if self.clipboard_stack.items_count():
            if isinstance(self.clipboard_stack.peek(), TextClipboardObject):
                QApplication.clipboard().setText(self.clipboard_stack.peek().text)
            if isinstance(self.clipboard_stack.peek(), ImageClipboardObject):
                QApplication.clipboard().setPixmap(self.clipboard_stack.peek().pixmap)

    @pyqtSlot()
    def _clipboard_changed(self):
        """Slot to be called when the state of the system's clipboard changes (mostly after copying)"""
        # current_text = Text.apply(QApplication.clipboard().text())
        current_text = QApplication.clipboard().text()
        current_image = QApplication.clipboard().pixmap()

        top_item = self.clipboard_stack.peek()

        # current_text = PT.apply(QApplication.clipboard().text()) # TODO: Chain plugins together
        print("Current Text:", QApplication.clipboard().text())
        print("Current Image Info:", QApplication.clipboard().pixmap())

        if current_text and (self._last_text is None or current_text != self._last_text) and \
                not (isinstance(top_item, TextClipboardObject) and top_item.text == current_text):
            self.clipboard_stack.push_item(TextClipboardObject(current_text))
            self.clipboard_changed_signal.emit(self.clipboard_stack)

        if not current_image.toImage().isNull() \
                and (self._last_image is None
                     or current_image.toImage() != self._last_image.toImage()) \
                and not (isinstance(top_item, ImageClipboardObject)
                         and top_item.pixmap.toImage() == current_image.toImage()):
            self.clipboard_stack.push_item(ImageClipboardObject(current_image))
            self.clipboard_changed_signal.emit(self.clipboard_stack)

        self._last_image = current_image
        self._last_text = current_text

    # DONE: use Qt signals properly
    # https://stackoverflow.com/questions/36434706/pyqt-proper-use-of-emit-and-pyqtsignal
    # def bind_clipboard_state_callback(self, function):
    #     self._clipboard_state_callback = function

    def set_selected_object(self, idx):
        if not 0 <= idx < self.clipboard_stack.items_count():
            raise Exception("Index is out of bounds")

        """Highlights a particular row in the main window"""
        self.clipboard_stack.set_current_item(idx)

    @pyqtSlot()
    def remove_clipboard_item(self):
        """Public function to remove a clipboard item"""
        self._remove_clipboard_item(self.clipboard_stack.current_item_idx)
        self.clipboard_changed_signal.emit(self.clipboard_stack)

    def move_selected_item_up(self):
        """Moves the current item in the stack up by one"""
        self.clipboard_stack.shift_current_item(Stack.SHIFT_DIRECTION.UP)
        self.stack_changed_signal.emit(self.clipboard_stack)

    def move_selected_item_down(self):
        """Moves the current item in the stack down by one"""
        self.clipboard_stack.shift_current_item(Stack.SHIFT_DIRECTION.DOWN)
        self.stack_changed_signal.emit(self.clipboard_stack)

    def _remove_clipboard_item(self, idx):
        """Helper function to remove a item from the stack"""
        if not self.clipboard_stack.items_count():
            return

        if not 0 <= idx < self.clipboard_stack.items_count():
            raise Exception("Index is out of bounds")

        self.clipboard_stack.pop(idx)
        self.stack_changed_signal.emit(self.clipboard_stack)
        # self.clipboard_changed_signal.emit(self.clipboard_stack)

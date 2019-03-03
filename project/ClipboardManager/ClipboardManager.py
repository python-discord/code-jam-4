"""Class encapsulating clipboard events"""
import logging

from PyQt5.Qt import QApplication  # noqa: F401
from PyQt5.QtCore import pyqtSignal, QObject, pyqtSlot

from project.ClipboardManager.ClipboardObject import TextClipboardObject, ImageClipboardObject
from project.ConfigManager import ConfigManager
from project.PluginManager import PluginManager
from project.Stack import Stack


# https://stackoverflow.com/questions/36522809/
# pyqt5-connection-doesnt-work-item-cannot-be-converted-to-pyqt5-qtcore-qobject
class ClipboardManager(QObject):
    clipboard_changed_signal = pyqtSignal(Stack)
    stack_changed_signal = pyqtSignal(Stack)

    def __init__(self):
        super().__init__()
        self._logger = logging.getLogger(self.__class__.__qualname__)

        self._plugin_manager = PluginManager()
        self._clipboard_state_callback = None
        self._last_text = None
        self._last_image = None

        self._clipboard_mutex = False

        QApplication.clipboard().dataChanged.connect(self._clipboard_changed)

        self.clipboard_stack = Stack()
        self.stack_changed_signal.connect(self._stack_changed)

    @pyqtSlot(Stack)
    def _stack_changed(self):
        """Slot to be called when the state of the stack changes
        (usually on add, move, delete, or moving items around """
        self._clipboard_mutex = True
        _config = ConfigManager.get_instance()

        # copy the top of the stack into the clipboard if the stack is not empty.
        if self.clipboard_stack.items_count():
            if _config.auto_load_top:
                item_to_load = self.clipboard_stack.peek()
            else:
                item_to_load = self.clipboard_stack.current_item

            if isinstance(item_to_load, TextClipboardObject):
                self._last_text = item_to_load.text
                self._logger.info("Current Stack Item: " + item_to_load.text)
                QApplication.clipboard().setText(item_to_load.text)
            elif isinstance(item_to_load, ImageClipboardObject):
                self._last_image = item_to_load.pixmap
                self._logger.info("Stack Changed Item: " + str(self._last_image))
                QApplication.clipboard().setPixmap(self._last_image)

    @pyqtSlot()
    def _clipboard_changed(self):
        """Slot to be called when the state of the system's clipboard changes
        (mostly after copying)"""
        self._logger.info("Clipboard Changed called")
        if self._clipboard_mutex:
            self._clipboard_mutex = False
            return

        current_text = QApplication.clipboard().text()
        current_image = QApplication.clipboard().pixmap()

        # current_text = PT.apply(QApplication.clipboard().text()) # TODO: Chain plugins together
        self._logger.info("Current Text:" + str(QApplication.clipboard().text()))
        self._logger.info("Current Image Info:" + str(QApplication.clipboard().pixmap()))

        if current_text and (self._last_text is None or current_text != self._last_text):
            self._plugin_manager.on_copy_text(current_text, self.clipboard_stack)
            self.clipboard_changed_signal.emit(self.clipboard_stack)

        # If the image is not blank
        if not current_image.toImage().isNull() \
                and (self._last_image is None
                     or current_image.toImage() != self._last_image.toImage()):
            self._plugin_manager.on_copy_image(current_image, self.clipboard_stack)
            self.clipboard_changed_signal.emit(self.clipboard_stack)

        self._last_image = current_image
        self._last_text = current_text

    # DONE: use Qt signals properly
    # https://stackoverflow.com/questions/36434706/pyqt-proper-use-of-emit-and-pyqtsignal

    @pyqtSlot(int)
    def set_selected_object(self, idx):
        """Highlights a particular row in the main window"""
        self._logger.info("set_selected_object called " + str(idx))
        if not 0 <= idx < self.clipboard_stack.items_count():
            raise Exception("Index is out of bounds")

        self.clipboard_stack.set_current_item(idx)
        self._stack_changed()

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

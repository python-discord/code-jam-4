"""Wrapper for the generated Python code in ui/emoji_picker.py."""

from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QCursor
from crocpad.ui.emoji_picker import Ui_EmojiPicker


class EmojiPicker(QDialog, Ui_EmojiPicker):
    """Wrapper for the generated Python code of Ui_EmojiPicker.

    Custom behaviour: show currently dialed symbol, and insert into document.
    """
    def __init__(self, cursor: QCursor):
        self.cursor = cursor
        super(EmojiPicker, self).__init__()
        self.setupUi(self)
        self.symbol = ''
        self.value = 0
        self.emoji_dial.sliderMoved.connect(self.dial_moved)
        self.emoji_insert_button.clicked.connect(self.insert)

    def dial_moved(self):
        """Update the symbol label when the dial has moved."""
        self.value = self.emoji_dial.value()
        self.symbol = chr(self.value)
        self.emoji_label.setText(self.symbol)

    def insert(self):
        """Insert the current symbol at the given cursor."""
        self.cursor.insertText(self.symbol)

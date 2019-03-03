"""Wrapper for the generated Python code in ui/emoji_picker.py."""

from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QCursor
from crocpad.ui.emoji_picker import Ui_EmojiPicker


class EmojiPicker(QDialog, Ui_EmojiPicker):
    """Wrapper for the generated Python code of Ui_EmojiPicker.

    Calls the inherited setupUi method to set up the layout that was done in Qt Designer.
    Custom behaviour: show currently dialed symbol, and insert into document.
    """

    def __init__(self, cursor: QCursor):
        super(EmojiPicker, self).__init__()
        self.setupUi(self)  # inherited method from the Designer file

        self.cursor = cursor
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

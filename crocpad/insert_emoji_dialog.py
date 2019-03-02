from PyQt5.QtWidgets import QDialog
from crocpad.ui.emoji_picker import Ui_EmojiPicker


class EmojiPicker(QDialog, Ui_EmojiPicker):
    def __init__(self, cursor):
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
        self.cursor.insertText(self.symbol)

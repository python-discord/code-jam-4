from PySide2.QtWidgets import QDialog

from project import ui


class SeekDialogue(QDialog):
    def __init__(self, *args, **kwargs):
        super(SeekDialogue, self).__init__(*args, **kwargs)

        self.ui = ui.SeekDialogue()
        self.ui.setupUi(self)

        self.ui.hour_dial.valueChanged.connect(lambda value: self.ui.hour_lcd.display(value))
        self.ui.min_dial.valueChanged.connect(lambda value: self.ui.min_lcd.display(value))
        self.ui.sec_dial.valueChanged.connect(lambda value: self.ui.sec_lcd.display(value))

    def get_position(self) -> int:
        """Return the selected position in milliseconds."""
        pos = self.ui.hour_dial.value() * 3.6e+6
        pos += self.ui.min_dial.value() * 60000
        pos += self.ui.sec_dial.value() * 1000

        return pos

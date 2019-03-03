from PySide2.QtWidgets import QDialog

from project import ui

# Constants in milliseconds
HOUR = 3600000
MINUTE = 60000
SECOND = 1000


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
        pos = self.ui.hour_dial.value() * HOUR
        pos += self.ui.min_dial.value() * MINUTE
        pos += self.ui.sec_dial.value() * SECOND

        return pos

    def update_duration(self, duration: int):
        """Set the maximum value of the dials and toggles widgets accordingly."""
        if duration >= MINUTE:
            self.ui.sec_dial.setMaximum(59)
            self.ui.min_dial.setEnabled(True)
            self.ui.min_lcd.setEnabled(True)
        else:
            self.ui.sec_dial.setMaximum(duration // SECOND)
            self.ui.min_dial.setEnabled(False)
            self.ui.min_lcd.setEnabled(False)

        if duration >= HOUR:
            self.ui.min_dial.setMaximum(59)
            self.ui.hour_dial.setEnabled(True)
            self.ui.hour_dial.setEnabled(True)
        else:
            self.ui.min_dial.setMaximum(duration // MINUTE)
            self.ui.hour_dial.setEnabled(False)
            self.ui.hour_dial.setEnabled(False)

        self.ui.hour_dial.setMaximum(duration // HOUR)

    def update_position(self, position: int):
        """Set the values of the dials."""
        hours, remainder = divmod(position, HOUR)
        self.ui.hour_dial.setValue(hours)

        minutes, remainder = divmod(remainder, MINUTE)
        self.ui.min_dial.setValue(minutes)

        self.ui.sec_dial.setValue(remainder // SECOND)

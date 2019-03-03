from PySide2.QtWidgets import QDialog

from project import ui


class SeekDialogue(QDialog):
    def __init__(self, *args, **kwargs):
        super(SeekDialogue, self).__init__(*args, **kwargs)

        self.ui = ui.SeekDialogue()
        self.ui.setupUi(self)

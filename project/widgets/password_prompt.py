from PySide2.QtWidgets import QWidget

from project import ui


class PasswordPrompt(QWidget):
    def __init__(self, *args, **kwargs):
        super(PasswordPrompt, self).__init__(*args, **kwargs)

        self.ui = ui.PasswordPrompt()
        self.ui.setupUi(self)

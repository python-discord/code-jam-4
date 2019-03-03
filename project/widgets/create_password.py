from PySide2.QtWidgets import QWidget

from project import ui


class CreatePassword(QWidget):
    def __init__(self, *args, **kwargs):
        super(CreatePassword, self).__init__(*args, **kwargs)

        self.ui = ui.CreatePassword()
        self.ui.setupUi(self)

        # self.password = password

        self.ui.confirm_button.pressed.connect(self.check)

    def check(self):
        raise NotImplementedError

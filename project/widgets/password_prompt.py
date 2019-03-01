from PySide2.QtWidgets import QWidget

from project import ui, password


class PasswordPrompt(QWidget):
    def __init__(self, *args, **kwargs):
        super(PasswordPrompt, self).__init__(*args, **kwargs)

        self.ui = ui.PasswordPrompt()
        self.ui.setupUi(self)

        self.ui.cancel_button.pressed.connect(self.close)
        self.ui.confirm_button.pressed.connect(self.check)

    def check(self):
        field_one = self.ui.password_regular.text()
        field_two = self.ui.password_backwards.text()
        if (field_one == password) and (field_two == password[::-1]):
            self.close()
            return 1
        else:
            self.ui.correct_label.setText('Password incorrect. Try again.')
            return 0

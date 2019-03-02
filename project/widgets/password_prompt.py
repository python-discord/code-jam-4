from PySide2.QtWidgets import QWidget
from random import choice

from project import ui


class PasswordPrompt(QWidget):
    def __init__(self, password, *args, **kwargs):
        super(PasswordPrompt, self).__init__(*args, **kwargs)

        self.password = password
        self.ui = ui.PasswordPrompt()
        self.ui.setupUi(self)

        self.ui.cancel_button.pressed.connect(self.close)
        self.ui.confirm_button.pressed.connect(self.check)
        self.success = False

    def change_password(self, new_password):
        self.password = new_password

    def display(self):
        self.success = False
        self.show()

    def check(self):
        """Check if entered passphrase is correct."""
        field_one = self.ui.password_regular.text()
        field_two = self.ui.password_backwards.text()
        if (field_one == self.password)) and \
           (field_two == sorted(self.password)):
            self.success = True
            self.close()
        else:
            self.ui.correct_label.setText(
                "<span style='color:red'>Passphrase incorrect. Try again.</span>"
            )

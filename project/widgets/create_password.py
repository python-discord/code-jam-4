from PySide2.QtWidgets import QWidget

from project import ui


class CreatePassword(QWidget):
    def __init__(self, *args, **kwargs):
        super(CreatePassword, self).__init__(*args, **kwargs)

        self.ui = ui.CreatePassword()
        self.ui.setupUi(self)

        self.ui.confirm_button.pressed.connect(self.check)
        self.new_password = ""

    def display(self):
        self.new_password = ""
        self.show()

    def closeEvent(self, event):
        if self.new_password == "":
            event.ignore()

    def check(self):
        password = self.ui.password.text()
        other = self.ui.confirm_password.text()
        error_message = ""
        if 9 < len(password) > 13:
            error_message += "Length of password must be between 10 and 12.\n"
        has_number, has_character, has_special = False, False, False
        for c in password:
            if c in "1234567890":
                has_number = True
            if c in "~!@#$%^&*()_+{}|:'<>?`-=\\;\",./[]":
                has_special = True
            if c.lower() in "abcdefghijklmnopqrstuvwxyz":
                has_character = True
        if not has_number:
            error_message += "Password must have at least one number.\n"
        if not has_character:
            error_message += "Password must have at least one alphabetical character.\n"
        if not has_special:
            error_message += "Password must have at least one special character.\n"
        if password != other[::-1]:
            error_message += "Confirmation must be backwards of the password."
        if error_message == "":
            self.new_password = password
            self.close()
        else:
            self.ui.error_message.setText(f"<span style='color:red'>{error_message}</span>")

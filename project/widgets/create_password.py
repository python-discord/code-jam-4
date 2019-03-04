import sys

from PySide2.QtWidgets import QDialog

from project import ui


class CreatePassword(QDialog):
    def __init__(self, *args, **kwargs):
        super(CreatePassword, self).__init__(*args, **kwargs)

        self.ui = ui.CreatePassword()
        self.ui.setupUi(self)

        self.ui.buttons.accepted.connect(self.accept)
        self.ui.buttons.rejected.connect(self.reject)
        self.new_password = ""

    def closeEvent(self, event):
        sys.exit()

    def open(self):
        self.new_password = ""
        super().open()

    def exec_(self):
        self.new_password = ""
        super().exec_()

    def done(self, result: QDialog.DialogCode):
        if result == QDialog.Accepted:
            errors = self._check()
            if errors:
                self.ui.error_message.setText(f"<span style='color:red'>{errors}</span>")
                return

        self.new_password = self.ui.password.text()
        self.ui.error_message.clear()
        self.ui.password.clear()
        self.ui.confirm_password.clear()

        super().done(result)

    def _check(self) -> str:
        """Check if the password is valid and return any error messages to be displayed."""
        password = self.ui.password.text()
        other = self.ui.confirm_password.text()
        error_message = ""

        if len(password) < 10 or len(password) > 12:
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

        return error_message

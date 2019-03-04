from PySide2.QtWidgets import QDialog

from project import ui


class PasswordPrompt(QDialog):
    def __init__(self, password, *args, **kwargs):
        super(PasswordPrompt, self).__init__(*args, **kwargs)

        self.ui = ui.PasswordPrompt()
        self.ui.setupUi(self)

        self.password = password

        self.ui.buttons.accepted.connect(self.accept)
        self.ui.buttons.rejected.connect(self.reject)

    def done(self, result: QDialog.DialogCode):
        if result == QDialog.Accepted:
            if not self._check():
                self.ui.error.setText(
                    f"<span style='color:red'>Passphrase incorrect. Try again.</span>"
                )
                return

        self.ui.error.clear()
        self.ui.password_input.clear()
        self.ui.confirm_input.clear()

        super().done(result)

    def _check(self) -> bool:
        """Check and return if the entered password is correct."""
        regular = self.ui.password_input.text()
        confirm = self.ui.confirm_input.text()
        return regular == self.password and confirm == "".join(sorted(self.password))

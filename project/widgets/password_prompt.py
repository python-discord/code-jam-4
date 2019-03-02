from PySide2.QtWidgets import QWidget
from random import choice

from project import ui

words = """
salty
fish
lackadaisical
lax
llama
lukewarm
leisurely
enthusiastic
fantastic
flying
alphabetical
gamma
terrier
excitable
green
purple
superb
stressed
machine
hunter
""".split('\n')[1:-1]


class PasswordPrompt(QWidget):
    def __init__(self, *args, **kwargs):
        super(PasswordPrompt, self).__init__(*args, **kwargs)

        self.ui = ui.PasswordPrompt()
        self.ui.setupUi(self)

        self.ui.cancel_button.pressed.connect(self.close)
        self.ui.confirm_button.pressed.connect(self.check)
        self.success = -1

    def display(self):
        self.success = -1
        self.passphrase = [choice(words), choice(words), choice(words)]
        self.ui.generated_passphrase.setText(
            f"Your generated passphrase is <b>{' '.join(self.passphrase)}</b>."
        )
        self.show()

    def check(self):
        """Check if entered passphrase is correct."""
        field_one = self.ui.password_regular.text()
        field_two = self.ui.password_backwards.text()
        if (field_one == ' '.join(sorted(self.passphrase))) and \
           (field_two == sorted(self.passphrase)[0][::-1]):
            self.success = 1
            self.close()
        else:
            self.ui.correct_label.setText(
                "<span style='color:red'>Passphrase incorrect. Try again.</span>"
            )

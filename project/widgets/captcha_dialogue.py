import random

from captcha.image import ImageCaptcha
from PySide2.QtCore import QByteArray
from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import QDialog, QGraphicsScene

from project import ui


CHARACTERS = "2345679ADEFGHJLMNQRTabdefgjmnqr"


class CaptchaDialogue(QDialog):
    def __init__(self, *args, **kwargs):
        super(CaptchaDialogue, self).__init__(*args, **kwargs)

        self.ui = ui.CaptchaDialogue()
        self.ui.setupUi(self)

        self.captcha_generator = ImageCaptcha()
        self.scene = QGraphicsScene()
        self.ui.captcha_view.setScene(self.scene)

        self.text = None

        self.ui.buttons.accepted.connect(self.accept)
        self.ui.buttons.rejected.connect(self.reject)

    def open(self):
        self.generate_captcha()
        super().open()

    def done(self, result: QDialog.DialogCode):
        if result == QDialog.Accepted and self.ui.captcha_input.text() != self.text:
            self.ui.input_label.setText("Incorrect CAPTCHA given. Try again:")
            self.ui.input_label.setStyleSheet("color: red")
            self.generate_captcha()
        else:
            self.ui.input_label.setText("Enter the characters displayed above:")
            self.ui.input_label.setStyleSheet("")
            self.ui.captcha_input.clear()
            super().done(result)

    def generate_captcha(self):
        self.text = self._generate_text()
        image_bytes = self.captcha_generator.generate(self.text).getvalue()
        image = QByteArray(image_bytes)

        pixmap = QPixmap()
        pixmap.loadFromData(image, "png")
        self.scene.clear()
        self.scene.addPixmap(pixmap)

    @staticmethod
    def _generate_text() -> str:
        """Return a string of random characters to be used for CAPTCHA generation."""
        sample = random.sample(CHARACTERS, 6)
        return "".join(sample)

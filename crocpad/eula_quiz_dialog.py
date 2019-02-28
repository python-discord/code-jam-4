from PyQt5.QtWidgets import QDialog
from crocpad.ui.eula_quiz import Ui_EulaQuizDialog
from PyQt5.QtCore import Qt


class EulaQuizDialog(QDialog, Ui_EulaQuizDialog):
    def __init__(self):
        super(EulaQuizDialog, self).__init__()
        self.setupUi(self)
        # Disable Help Menu, Close Button and System Menu
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowCloseButtonHint)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowSystemMenuHint)

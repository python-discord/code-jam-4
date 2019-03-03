"""Wrapper for the generated Python code in ui/eula_quiz.py."""

from PyQt5.QtWidgets import QDialog
from crocpad.ui.eula_quiz import Ui_EulaQuizDialog
from PyQt5.QtCore import Qt


class EulaQuizDialog(QDialog, Ui_EulaQuizDialog):
    """Wrapper for the generated Python code of Ui_EulaQuizDialog.

    Custom behaviour: disabled some ways of evading the dialog.
    """
    def __init__(self):
        super(EulaQuizDialog, self).__init__()
        self.setupUi(self)
        # Disable Help Menu, Close Button and System Menu
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowCloseButtonHint)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowSystemMenuHint)

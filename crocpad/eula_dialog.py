"""Wrapper for the generated Python code in ui/eula.py."""

from PyQt5.QtWidgets import QDialog
from crocpad.ui.eula import Ui_EulaDialog
from PyQt5.QtCore import Qt


class EulaDialog(QDialog, Ui_EulaDialog):
    """Wrapper for the generated Python code of Ui_EulaDialog.

    Custom behaviour: disabled some ways of evading the dialog.
    """
    def __init__(self, eula: str):
        super(EulaDialog, self).__init__()
        self.setupUi(self)
        self.eula_TextEdit.setPlainText(eula)
        # Disable Help Menu, Close Button and System Menu
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowCloseButtonHint)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowSystemMenuHint)

"""Wrapper for the generated Python code in ui/eula.py."""

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import Qt
from crocpad.ui.eula import Ui_EulaDialog


class EulaDialog(QDialog, Ui_EulaDialog):
    """Wrapper for the generated Python code of Ui_EulaDialog.

    Calls the inherited setupUi method to set up the layout that was done in Qt Designer.
    Custom behaviour:
        count scrollbar movements
        behaviours for Disagree and Agree buttons
        disabled some ways of evading the dialog
    """

    def __init__(self, eula: str):
        super(EulaDialog, self).__init__()
        self.setupUi(self)  # inherited method from the Designer file

        self.eula_TextEdit.setPlainText(eula)
        self.eula_TextEdit.ensureCursorVisible()
        self.clicked_button = None
        self.scrolled_to_bottom = 0
        self.scrolled_to_top = 0
        self.eula_agree_button.clicked.connect(self.clicked_agree)
        self.eula_disagree_button.clicked.connect(self.clicked_disagree)
        self.eula_TextEdit.verticalScrollBar().sliderMoved.connect(self.slider_moved)
        self.eula_agree_button.setEnabled(False)  # disable the Agree button until conditions met

        # Disable Help Menu, Close Button and System Menu
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowCloseButtonHint)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowSystemMenuHint)

    def slider_moved(self):
        """Count the number of times the scrollbar has hit top and bottom."""
        current = self.eula_TextEdit.verticalScrollBar().value()
        maximum = self.eula_TextEdit.verticalScrollBar().maximum()
        minimum = self.eula_TextEdit.verticalScrollBar().minimum()
        if current == maximum:
            self.scrolled_to_bottom += 1
            if self.scrolled_to_bottom >= 3 and self.scrolled_to_top >= 2:
                self.eula_agree_button.setEnabled(True)
        if current == minimum:
            self.scrolled_to_top += 1

    def clicked_disagree(self):
        """Process a click on the Disagree button."""
        dlg = QtWidgets.QMessageBox(self)
        dlg.setText("I believe you meant to select AGREE.")
        dlg.setIcon(QtWidgets.QMessageBox.Critical)
        dlg.show()

    def clicked_agree(self):
        """Process a click on the Agree button.

        No gatekeeping is required here since the button was disabled until conditions were met.
        """
        self.clicked_button = self.eula_agree_button
        self.close()

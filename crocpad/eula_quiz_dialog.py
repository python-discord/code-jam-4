"""Wrapper for the generated Python code in ui/eula_quiz.py."""

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import Qt
from crocpad.ui.eula_quiz import Ui_EulaQuizDialog


class EulaQuizDialog(QDialog, Ui_EulaQuizDialog):
    """Wrapper for the generated Python code of Ui_EulaQuizDialog.

    Calls the inherited setupUi method to set up the layout that was done in Qt Designer.
    Custom behaviour:
        group radio buttons
        check quiz answers when Submit clicked
        disabled some ways of evading the dialog.
    """
    def __init__(self):
        super(EulaQuizDialog, self).__init__()
        self.setupUi(self)  # inherited method from the Designer file

        self.submitButton.clicked.connect(self.submit_clicked)

        # Set up button groups: otherwise only one radio button can be selected at once.
        self.group_1 = QtWidgets.QButtonGroup()
        self.group_2 = QtWidgets.QButtonGroup()
        self.group_3 = QtWidgets.QButtonGroup()
        self.group_4 = QtWidgets.QButtonGroup()
        self.group_5 = QtWidgets.QButtonGroup()
        self.group_6 = QtWidgets.QButtonGroup()
        # Only the "correct" buttons were given non-default names in Qt Designer.
        self.group_1.addButton(self.radioButton_16)
        self.group_1.addButton(self.quiz1_Correct)
        self.group_1.addButton(self.radioButton_18)
        self.group_1.addButton(self.radioButton_19)
        self.group_1.addButton(self.radioButton_20)
        self.group_2.addButton(self.radioButton_11)
        self.group_2.addButton(self.radioButton_12)
        self.group_2.addButton(self.radioButton_13)
        self.group_2.addButton(self.radioButton_14)
        self.group_2.addButton(self.quiz2_Correct)
        self.group_3.addButton(self.radioButton)
        self.group_3.addButton(self.radioButton_2)
        self.group_3.addButton(self.radioButton_3)
        self.group_3.addButton(self.radioButton_4)
        self.group_3.addButton(self.quiz3_Correct)
        self.group_4.addButton(self.radioButton_21)
        self.group_4.addButton(self.radioButton_22)
        self.group_4.addButton(self.radioButton_23)
        self.group_4.addButton(self.radioButton_24)
        self.group_4.addButton(self.quiz4_Correct)
        self.group_5.addButton(self.radioButton_26)
        self.group_5.addButton(self.radioButton_27)
        self.group_5.addButton(self.quiz5_Correct)
        self.group_5.addButton(self.radioButton_29)
        self.group_5.addButton(self.radioButton_30)
        self.group_6.addButton(self.radioButton_31)
        self.group_6.addButton(self.radioButton_32)
        self.group_6.addButton(self.radioButton_33)
        self.group_6.addButton(self.radioButton_34)
        self.group_6.addButton(self.quiz6_Correct)

        # Disable Help Menu, Close Button and System Menu
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowCloseButtonHint)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowSystemMenuHint)

    def submit_clicked(self):
        """Process a click on the Submit button.

        If the correct answers were all selected, the user is allowed to continue."""
        if self.quiz_correct():
            dlg = QtWidgets.QMessageBox(self)
            dlg.setText("Correct. Thank you for using Crocpad++.")
            dlg.setIcon(QtWidgets.QMessageBox.Critical)
            dlg.show()
        self.close()

    def quiz_correct(self) -> bool:
        """Return True if the correct answers are all currently selected, False otherwise."""
        return (self.quiz1_Correct.isChecked() and
                self.quiz2_Correct.isChecked() and
                self.quiz3_Correct.isChecked() and
                self.quiz4_Correct.isChecked() and
                self.quiz5_Correct.isChecked() and
                self.quiz6_Correct.isChecked()
                )

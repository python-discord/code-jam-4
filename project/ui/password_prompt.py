# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt/passwordprompt.ui',
# licensing of 'qt/passwordprompt.ui' applies.
#
# Created: Sat Mar  2 13:02:35 2019
#      by: pyside2-uic  running on PySide2 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_PasswordPrompt(object):
    def setupUi(self, PasswordPrompt):
        PasswordPrompt.setObjectName("PasswordPrompt")
        PasswordPrompt.resize(400, 300)
        self.instructions = QtWidgets.QTextBrowser(PasswordPrompt)
        self.instructions.setGeometry(QtCore.QRect(10, 60, 381, 41))
        self.instructions.setObjectName("instructions")
        self.instructions_backwards = QtWidgets.QTextBrowser(PasswordPrompt)
        self.instructions_backwards.setGeometry(QtCore.QRect(10, 140, 381, 41))
        self.instructions_backwards.setObjectName("instructions_backwards")
        self.password_label = QtWidgets.QLabel(PasswordPrompt)
        self.password_label.setGeometry(QtCore.QRect(10, 110, 71, 20))
        self.password_label.setObjectName("password_label")
        self.password_regular = QtWidgets.QLineEdit(PasswordPrompt)
        self.password_regular.setGeometry(QtCore.QRect(60, 110, 321, 20))
        self.password_regular.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_regular.setObjectName("password_regular")
        self.password_label_2 = QtWidgets.QLabel(PasswordPrompt)
        self.password_label_2.setGeometry(QtCore.QRect(10, 190, 71, 20))
        self.password_label_2.setObjectName("password_label_2")
        self.password_backwards = QtWidgets.QLineEdit(PasswordPrompt)
        self.password_backwards.setGeometry(QtCore.QRect(60, 190, 321, 20))
        self.password_backwards.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_backwards.setObjectName("password_backwards")
        self.confirm_button = QtWidgets.QPushButton(PasswordPrompt)
        self.confirm_button.setGeometry(QtCore.QRect(240, 270, 75, 23))
        self.confirm_button.setObjectName("confirm_button")
        self.cancel_button = QtWidgets.QPushButton(PasswordPrompt)
        self.cancel_button.setGeometry(QtCore.QRect(320, 270, 75, 23))
        self.cancel_button.setObjectName("cancel_button")
        self.correct_label = QtWidgets.QLabel(PasswordPrompt)
        self.correct_label.setGeometry(QtCore.QRect(10, 230, 381, 20))
        self.correct_label.setText("")
        self.correct_label.setObjectName("correct_label")
        self.generated_passphrase = QtWidgets.QLabel(PasswordPrompt)
        self.generated_passphrase.setGeometry(QtCore.QRect(10, 20, 381, 20))
        self.generated_passphrase.setText("")
        self.generated_passphrase.setObjectName("generated_passphrase")

        self.retranslateUi(PasswordPrompt)
        QtCore.QMetaObject.connectSlotsByName(PasswordPrompt)

    def retranslateUi(self, PasswordPrompt):
        PasswordPrompt.setWindowTitle(QtWidgets.QApplication.translate("PasswordPrompt", "Form", None, -1))
        self.instructions.setHtml(QtWidgets.QApplication.translate("PasswordPrompt", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Please reorder the passphrase into alphabetical order.</p></body></html>", None, -1))
        self.instructions_backwards.setHtml(QtWidgets.QApplication.translate("PasswordPrompt", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Enter the alphabetically foremost word of the passphrase, but backwards.</p></body></html>", None, -1))
        self.password_label.setText(QtWidgets.QApplication.translate("PasswordPrompt", "Password", None, -1))
        self.password_label_2.setText(QtWidgets.QApplication.translate("PasswordPrompt", "Password", None, -1))
        self.confirm_button.setText(QtWidgets.QApplication.translate("PasswordPrompt", "Confirm", None, -1))
        self.cancel_button.setText(QtWidgets.QApplication.translate("PasswordPrompt", "Cancel", None, -1))


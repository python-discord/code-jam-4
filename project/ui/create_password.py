# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt/createpassword.ui',
# licensing of 'qt/createpassword.ui' applies.
#
# Created: Sun Mar  3 09:26:31 2019
#      by: pyside2-uic  running on PySide2 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_CreatePassword(object):
    def setupUi(self, CreatePassword):
        CreatePassword.setObjectName("CreatePassword")
        CreatePassword.resize(400, 300)
        self.textBrowser = QtWidgets.QTextBrowser(CreatePassword)
        self.textBrowser.setGeometry(QtCore.QRect(10, 10, 381, 61))
        self.textBrowser.setObjectName("textBrowser")
        self.password = QtWidgets.QLineEdit(CreatePassword)
        self.password.setGeometry(QtCore.QRect(80, 100, 311, 20))
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password.setObjectName("password")
        self.confirm_password = QtWidgets.QLineEdit(CreatePassword)
        self.confirm_password.setGeometry(QtCore.QRect(80, 130, 311, 20))
        self.confirm_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirm_password.setObjectName("confirm_password")
        self.label_2 = QtWidgets.QLabel(CreatePassword)
        self.label_2.setGeometry(QtCore.QRect(20, 122, 47, 31))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(CreatePassword)
        self.label_3.setGeometry(QtCore.QRect(20, 90, 47, 31))
        self.label_3.setObjectName("label_3")
        self.confirm_button = QtWidgets.QPushButton(CreatePassword)
        self.confirm_button.setGeometry(QtCore.QRect(320, 270, 75, 23))
        self.confirm_button.setObjectName("confirm_button")
        self.error_message = QtWidgets.QTextBrowser(CreatePassword)
        self.error_message.setGeometry(QtCore.QRect(10, 180, 381, 61))
        self.error_message.setObjectName("error_message")

        self.retranslateUi(CreatePassword)
        QtCore.QMetaObject.connectSlotsByName(CreatePassword)

    def retranslateUi(self, CreatePassword):
        CreatePassword.setWindowTitle(QtWidgets.QApplication.translate("CreatePassword", "Form", None, -1))
        self.textBrowser.setHtml(QtWidgets.QApplication.translate("CreatePassword", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Enter what you want your new password to be. To confirm what you entered, type your password backwards again.</p></body></html>", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("CreatePassword", "Confirm", None, -1))
        self.label_3.setText(QtWidgets.QApplication.translate("CreatePassword", "Password", None, -1))
        self.confirm_button.setText(QtWidgets.QApplication.translate("CreatePassword", "Confirm", None, -1))
        self.error_message.setHtml(QtWidgets.QApplication.translate("CreatePassword", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None, -1))

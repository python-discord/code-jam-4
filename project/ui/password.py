# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt/password.ui',
# licensing of 'qt/password.ui' applies.
#
# Created: Tue Feb 26 18:56:11 2019
#      by: pyside2-uic  running on PySide2 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_password(object):
    def setupUi(self, password):
        password.setObjectName("password")
        password.resize(400, 300)
        self.textBrowser = QtWidgets.QTextBrowser(password)
        self.textBrowser.setGeometry(QtCore.QRect(10, 10, 381, 41))
        self.textBrowser.setObjectName("textBrowser")
        self.textBrowser_2 = QtWidgets.QTextBrowser(password)
        self.textBrowser_2.setGeometry(QtCore.QRect(10, 120, 381, 41))
        self.textBrowser_2.setObjectName("textBrowser_2")
        self.label = QtWidgets.QLabel(password)
        self.label.setGeometry(QtCore.QRect(10, 70, 71, 20))
        self.label.setObjectName("label")
        self.password_regular = QtWidgets.QLineEdit(password)
        self.password_regular.setGeometry(QtCore.QRect(60, 70, 321, 20))
        self.password_regular.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_regular.setObjectName("password_regular")
        self.label_2 = QtWidgets.QLabel(password)
        self.label_2.setGeometry(QtCore.QRect(10, 180, 71, 20))
        self.label_2.setObjectName("label_2")
        self.password_backwards = QtWidgets.QLineEdit(password)
        self.password_backwards.setGeometry(QtCore.QRect(60, 180, 321, 20))
        self.password_backwards.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_backwards.setObjectName("password_backwards")
        self.confirm = QtWidgets.QPushButton(password)
        self.confirm.setGeometry(QtCore.QRect(320, 270, 75, 23))
        self.confirm.setObjectName("confirm")

        self.retranslateUi(password)
        QtCore.QMetaObject.connectSlotsByName(password)

    def retranslateUi(self, password):
        password.setWindowTitle(QtWidgets.QApplication.translate("password", "Form", None, -1))
        self.textBrowser.setHtml(QtWidgets.QApplication.translate("password", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Please enter your password as a security precaution.</p></body></html>", None, -1))
        self.textBrowser_2.setHtml(QtWidgets.QApplication.translate("password", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Enter your password again but backwards.</p></body></html>", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("password", "Password", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("password", "Password", None, -1))
        self.confirm.setText(QtWidgets.QApplication.translate("password", "Confirm", None, -1))


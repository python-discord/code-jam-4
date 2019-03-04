# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt/createpassword.ui',
# licensing of 'qt/createpassword.ui' applies.
#
# Created: Sun Mar  3 14:56:24 2019
#      by: pyside2-uic  running on PySide2 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_CreatePassword(object):
    def setupUi(self, CreatePassword):
        CreatePassword.setObjectName("CreatePassword")
        CreatePassword.setWindowModality(QtCore.Qt.ApplicationModal)
        CreatePassword.resize(400, 300)
        CreatePassword.setMinimumSize(QtCore.QSize(400, 300))
        CreatePassword.setModal(True)
        self.formLayout = QtWidgets.QFormLayout(CreatePassword)
        self.formLayout.setContentsMargins(10, 10, 10, 10)
        self.formLayout.setSpacing(15)
        self.formLayout.setObjectName("formLayout")
        self.instructions = QtWidgets.QTextBrowser(CreatePassword)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.instructions.sizePolicy().hasHeightForWidth())
        self.instructions.setSizePolicy(sizePolicy)
        self.instructions.setObjectName("instructions")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.SpanningRole, self.instructions)
        self.password_label = QtWidgets.QLabel(CreatePassword)
        self.password_label.setMargin(4)
        self.password_label.setObjectName("password_label")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.password_label)
        self.password = QtWidgets.QLineEdit(CreatePassword)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password.setObjectName("password")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.password)
        self.confirm_label = QtWidgets.QLabel(CreatePassword)
        self.confirm_label.setMargin(4)
        self.confirm_label.setObjectName("confirm_label")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.confirm_label)
        self.confirm_password = QtWidgets.QLineEdit(CreatePassword)
        self.confirm_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirm_password.setObjectName("confirm_password")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.confirm_password)
        self.error_message = QtWidgets.QTextBrowser(CreatePassword)
        self.error_message.setObjectName("error_message")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.SpanningRole, self.error_message)
        self.buttons = QtWidgets.QDialogButtonBox(CreatePassword)
        self.buttons.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttons.setObjectName("buttons")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.SpanningRole, self.buttons)

        self.retranslateUi(CreatePassword)
        QtCore.QMetaObject.connectSlotsByName(CreatePassword)

    def retranslateUi(self, CreatePassword):
        CreatePassword.setWindowTitle(QtWidgets.QApplication.translate("CreatePassword", "Form", None, -1))
        self.instructions.setHtml(QtWidgets.QApplication.translate("CreatePassword", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Enter what you want your new password to be. To confirm what you entered, type your password backwards again.</p></body></html>", None, -1))
        self.password_label.setText(QtWidgets.QApplication.translate("CreatePassword", "Password:", None, -1))
        self.confirm_label.setText(QtWidgets.QApplication.translate("CreatePassword", "Confirm:", None, -1))
        self.error_message.setHtml(QtWidgets.QApplication.translate("CreatePassword", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None, -1))


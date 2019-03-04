# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt/passwordprompt.ui',
# licensing of 'qt/passwordprompt.ui' applies.
#
# Created: Sun Mar  3 15:23:43 2019
#      by: pyside2-uic  running on PySide2 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_PasswordPrompt(object):
    def setupUi(self, PasswordPrompt):
        PasswordPrompt.setObjectName("PasswordPrompt")
        PasswordPrompt.resize(350, 250)
        PasswordPrompt.setMinimumSize(QtCore.QSize(300, 250))
        self.formLayout = QtWidgets.QFormLayout(PasswordPrompt)
        self.formLayout.setContentsMargins(10, 10, 10, 10)
        self.formLayout.setSpacing(10)
        self.formLayout.setObjectName("formLayout")
        self.instructions = QtWidgets.QTextBrowser(PasswordPrompt)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.instructions.sizePolicy().hasHeightForWidth())
        self.instructions.setSizePolicy(sizePolicy)
        self.instructions.setObjectName("instructions")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.SpanningRole, self.instructions)
        self.password_label = QtWidgets.QLabel(PasswordPrompt)
        self.password_label.setMargin(4)
        self.password_label.setObjectName("password_label")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.password_label)
        self.password_input = QtWidgets.QLineEdit(PasswordPrompt)
        self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_input.setObjectName("password_input")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.password_input)
        self.confirm_instructions = QtWidgets.QTextBrowser(PasswordPrompt)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.confirm_instructions.sizePolicy().hasHeightForWidth())
        self.confirm_instructions.setSizePolicy(sizePolicy)
        self.confirm_instructions.setObjectName("confirm_instructions")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.SpanningRole, self.confirm_instructions)
        self.confirm_label = QtWidgets.QLabel(PasswordPrompt)
        self.confirm_label.setMargin(4)
        self.confirm_label.setObjectName("confirm_label")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.confirm_label)
        self.confirm_input = QtWidgets.QLineEdit(PasswordPrompt)
        self.confirm_input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirm_input.setObjectName("confirm_input")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.confirm_input)
        self.error = QtWidgets.QLabel(PasswordPrompt)
        self.error.setText("")
        self.error.setObjectName("error")
        self.formLayout.setWidget(8, QtWidgets.QFormLayout.SpanningRole, self.error)
        self.buttons = QtWidgets.QDialogButtonBox(PasswordPrompt)
        self.buttons.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttons.setObjectName("buttons")
        self.formLayout.setWidget(9, QtWidgets.QFormLayout.SpanningRole, self.buttons)

        self.retranslateUi(PasswordPrompt)
        QtCore.QMetaObject.connectSlotsByName(PasswordPrompt)

    def retranslateUi(self, PasswordPrompt):
        PasswordPrompt.setWindowTitle(QtWidgets.QApplication.translate("PasswordPrompt", "Enter Password", None, -1))
        self.instructions.setHtml(QtWidgets.QApplication.translate("PasswordPrompt", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">As a security precaution, please enter the password.</p></body></html>", None, -1))
        self.password_label.setText(QtWidgets.QApplication.translate("PasswordPrompt", "Password", None, -1))
        self.confirm_instructions.setHtml(QtWidgets.QApplication.translate("PasswordPrompt", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Please reorder the password into alphabetical order.</p></body></html>", None, -1))
        self.confirm_label.setText(QtWidgets.QApplication.translate("PasswordPrompt", "Password", None, -1))


# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt/captchadialogue.ui',
# licensing of 'qt/captchadialogue.ui' applies.
#
# Created: Sun Mar  3 12:16:41 2019
#      by: pyside2-uic  running on PySide2 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_CaptchaDialogue(object):
    def setupUi(self, CaptchaDialogue):
        CaptchaDialogue.setObjectName("CaptchaDialogue")
        CaptchaDialogue.setWindowModality(QtCore.Qt.ApplicationModal)
        CaptchaDialogue.resize(300, 275)
        CaptchaDialogue.setMinimumSize(QtCore.QSize(300, 275))
        self.gridLayout = QtWidgets.QGridLayout(CaptchaDialogue)
        self.gridLayout.setSpacing(5)
        self.gridLayout.setContentsMargins(15, 15, 15, 15)
        self.gridLayout.setObjectName("gridLayout")
        self.captcha_view = QtWidgets.QGraphicsView(CaptchaDialogue)
        self.captcha_view.setObjectName("captcha_view")
        self.gridLayout.addWidget(self.captcha_view, 0, 0, 1, 3)
        self.buttons = QtWidgets.QDialogButtonBox(CaptchaDialogue)
        self.buttons.setOrientation(QtCore.Qt.Horizontal)
        self.buttons.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttons.setCenterButtons(True)
        self.buttons.setObjectName("buttons")
        self.gridLayout.addWidget(self.buttons, 6, 0, 1, 3)
        self.captcha_input = QtWidgets.QLineEdit(CaptchaDialogue)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.captcha_input.sizePolicy().hasHeightForWidth())
        self.captcha_input.setSizePolicy(sizePolicy)
        self.captcha_input.setObjectName("captcha_input")
        self.gridLayout.addWidget(self.captcha_input, 3, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 3)
        spacerItem1 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 4, 0, 1, 3)
        spacerItem2 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 3, 0, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem3, 3, 2, 1, 1)
        self.input_label = QtWidgets.QLabel(CaptchaDialogue)
        self.input_label.setScaledContents(False)
        self.input_label.setAlignment(QtCore.Qt.AlignCenter)
        self.input_label.setMargin(2)
        self.input_label.setObjectName("input_label")
        self.gridLayout.addWidget(self.input_label, 2, 0, 1, 3)

        self.retranslateUi(CaptchaDialogue)
        QtCore.QMetaObject.connectSlotsByName(CaptchaDialogue)

    def retranslateUi(self, CaptchaDialogue):
        CaptchaDialogue.setWindowTitle(QtWidgets.QApplication.translate("CaptchaDialogue", "CAPTCHA", None, -1))
        self.input_label.setText(QtWidgets.QApplication.translate("CaptchaDialogue", "Enter the characters displayed above:", None, -1))


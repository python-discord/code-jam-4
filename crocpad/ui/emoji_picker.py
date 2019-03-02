# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'emoji_picker.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_EmojiPicker(object):
    def setupUi(self, EmojiPicker):
        EmojiPicker.setObjectName("EmojiPicker")
        EmojiPicker.resize(422, 480)
        EmojiPicker.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.emoji_dial = QtWidgets.QDial(EmojiPicker)
        self.emoji_dial.setGeometry(QtCore.QRect(10, 60, 401, 411))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.emoji_dial.sizePolicy().hasHeightForWidth())
        self.emoji_dial.setSizePolicy(sizePolicy)
        self.emoji_dial.setBaseSize(QtCore.QSize(0, 0))
        self.emoji_dial.setCursor(QtGui.QCursor(QtCore.Qt.ClosedHandCursor))
        self.emoji_dial.setMouseTracking(False)
        self.emoji_dial.setAutoFillBackground(False)
        self.emoji_dial.setMaximum(9983)
        self.emoji_dial.setPageStep(1)
        self.emoji_dial.setOrientation(QtCore.Qt.Horizontal)
        self.emoji_dial.setInvertedAppearance(False)
        self.emoji_dial.setInvertedControls(False)
        self.emoji_dial.setWrapping(True)
        self.emoji_dial.setNotchTarget(50.0)
        self.emoji_dial.setNotchesVisible(False)
        self.emoji_dial.setObjectName("emoji_dial")
        self.emoji_insert_button = QtWidgets.QPushButton(EmojiPicker)
        self.emoji_insert_button.setGeometry(QtCore.QRect(150, 450, 126, 23))
        self.emoji_insert_button.setObjectName("emoji_insert_button")
        self.frame = QtWidgets.QFrame(EmojiPicker)
        self.frame.setGeometry(QtCore.QRect(140, 10, 141, 80))
        self.frame.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.frame.setFrameShape(QtWidgets.QFrame.Box)
        self.frame.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.frame.setObjectName("frame")
        self.emoji_label = QtWidgets.QLabel(self.frame)
        self.emoji_label.setGeometry(QtCore.QRect(30, 10, 81, 61))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Symbol")
        font.setPointSize(36)
        self.emoji_label.setFont(font)
        self.emoji_label.setText("")
        self.emoji_label.setAlignment(QtCore.Qt.AlignCenter)
        self.emoji_label.setObjectName("emoji_label")

        self.retranslateUi(EmojiPicker)
        QtCore.QMetaObject.connectSlotsByName(EmojiPicker)

    def retranslateUi(self, EmojiPicker):
        _translate = QtCore.QCoreApplication.translate
        EmojiPicker.setWindowTitle(_translate("EmojiPicker", "Insert symbol"))
        self.emoji_insert_button.setText(_translate("EmojiPicker", "Insert"))


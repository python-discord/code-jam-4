# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt/removedialogue.ui',
# licensing of 'qt/removedialogue.ui' applies.
#
# Created: Sun Mar  3 15:53:35 2019
#      by: pyside2-uic  running on PySide2 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_RemoveDialogue(object):
    def setupUi(self, RemoveDialogue):
        RemoveDialogue.setObjectName("RemoveDialogue")
        RemoveDialogue.setWindowModality(QtCore.Qt.WindowModal)
        RemoveDialogue.resize(409, 125)
        RemoveDialogue.setMinimumSize(QtCore.QSize(400, 125))
        RemoveDialogue.setModal(True)
        self.grid = QtWidgets.QGridLayout(RemoveDialogue)
        self.grid.setSpacing(10)
        self.grid.setContentsMargins(10, 10, 10, 10)
        self.grid.setObjectName("grid")
        self.buttons = QtWidgets.QDialogButtonBox(RemoveDialogue)
        self.buttons.setOrientation(QtCore.Qt.Horizontal)
        self.buttons.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttons.setCenterButtons(True)
        self.buttons.setObjectName("buttons")
        self.grid.addWidget(self.buttons, 2, 0, 1, 1)
        self.label = QtWidgets.QLabel(RemoveDialogue)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setMargin(4)
        self.label.setObjectName("label")
        self.grid.addWidget(self.label, 0, 0, 1, 1)
        self.input = QtWidgets.QLineEdit(RemoveDialogue)
        self.input.setObjectName("input")
        self.grid.addWidget(self.input, 1, 0, 1, 1)

        self.retranslateUi(RemoveDialogue)
        QtCore.QObject.connect(self.buttons, QtCore.SIGNAL("accepted()"), RemoveDialogue.accept)
        QtCore.QObject.connect(self.buttons, QtCore.SIGNAL("rejected()"), RemoveDialogue.reject)
        QtCore.QMetaObject.connectSlotsByName(RemoveDialogue)

    def retranslateUi(self, RemoveDialogue):
        RemoveDialogue.setWindowTitle(QtWidgets.QApplication.translate("RemoveDialogue", "Confirm Media Removal", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("RemoveDialogue", "Please enter the title of the media to confirm removal:", None, -1))


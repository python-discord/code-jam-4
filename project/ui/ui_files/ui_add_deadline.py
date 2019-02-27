# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_add_deadline.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets


class Ui_deadline_form(object):
    def setupUi(self, deadline_form):
        deadline_form.setObjectName("deadline_form")
        deadline_form.resize(500, 374)
        self.gridLayout = QtWidgets.QGridLayout(deadline_form)
        self.gridLayout.setObjectName("gridLayout")
        self.comboBox_8 = QtWidgets.QComboBox(deadline_form)
        self.comboBox_8.setObjectName("comboBox_8")
        self.gridLayout.addWidget(self.comboBox_8, 0, 7, 1, 1)
        self.comboBox_2 = QtWidgets.QComboBox(deadline_form)
        self.comboBox_2.setObjectName("comboBox_2")
        self.gridLayout.addWidget(self.comboBox_2, 0, 1, 1, 1)
        self.comboBox = QtWidgets.QComboBox(deadline_form)
        self.comboBox.setObjectName("comboBox")
        self.gridLayout.addWidget(self.comboBox, 0, 0, 1, 1)
        self.comboBox_9 = QtWidgets.QComboBox(deadline_form)
        self.comboBox_9.setObjectName("comboBox_9")
        self.gridLayout.addWidget(self.comboBox_9, 0, 8, 1, 1)
        self.comboBox_5 = QtWidgets.QComboBox(deadline_form)
        self.comboBox_5.setObjectName("comboBox_5")
        self.gridLayout.addWidget(self.comboBox_5, 0, 4, 1, 1)
        self.comboBox_4 = QtWidgets.QComboBox(deadline_form)
        self.comboBox_4.setObjectName("comboBox_4")
        self.gridLayout.addWidget(self.comboBox_4, 0, 3, 1, 1)
        self.comboBox_7 = QtWidgets.QComboBox(deadline_form)
        self.comboBox_7.setObjectName("comboBox_7")
        self.gridLayout.addWidget(self.comboBox_7, 0, 6, 1, 1)
        self.comboBox_6 = QtWidgets.QComboBox(deadline_form)
        self.comboBox_6.setObjectName("comboBox_6")
        self.gridLayout.addWidget(self.comboBox_6, 0, 5, 1, 1)
        self.comboBox_3 = QtWidgets.QComboBox(deadline_form)
        self.comboBox_3.setObjectName("comboBox_3")
        self.gridLayout.addWidget(self.comboBox_3, 0, 2, 1, 1)
        self.comboBox_10 = QtWidgets.QComboBox(deadline_form)
        self.comboBox_10.setObjectName("comboBox_10")
        self.gridLayout.addWidget(self.comboBox_10, 0, 9, 1, 1)

        self.retranslateUi(deadline_form)
        QtCore.QMetaObject.connectSlotsByName(deadline_form)

    def retranslateUi(self, deadline_form):
        _translate = QtCore.QCoreApplication.translate
        deadline_form.setWindowTitle(
            _translate("deadline_form", "Task Deadline"))

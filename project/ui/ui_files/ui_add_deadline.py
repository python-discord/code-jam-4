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
        deadline_form.resize(935, 374)
        self.gridLayout = QtWidgets.QGridLayout(deadline_form)
        self.gridLayout.setObjectName("gridLayout")
        self.comboBox_9 = QtWidgets.QComboBox(deadline_form)
        self.comboBox_9.setObjectName("comboBox_9")
        self.gridLayout.addWidget(self.comboBox_9, 2, 8, 1, 1)
        self.comboBox_10 = QtWidgets.QComboBox(deadline_form)
        self.comboBox_10.setObjectName("comboBox_10")
        self.gridLayout.addWidget(self.comboBox_10, 2, 9, 1, 1)
        self.comboBox_5 = QtWidgets.QComboBox(deadline_form)
        self.comboBox_5.setObjectName("comboBox_5")
        self.gridLayout.addWidget(self.comboBox_5, 2, 4, 1, 1)
        self.comboBox_7 = QtWidgets.QComboBox(deadline_form)
        self.comboBox_7.setObjectName("comboBox_7")
        self.gridLayout.addWidget(self.comboBox_7, 2, 6, 1, 1)
        self.comboBox_4 = QtWidgets.QComboBox(deadline_form)
        self.comboBox_4.setObjectName("comboBox_4")
        self.gridLayout.addWidget(self.comboBox_4, 2, 3, 1, 1)
        self.label = QtWidgets.QLabel(deadline_form)
        self.label.setBaseSize(QtCore.QSize(0, 0))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 10)
        self.comboBox_2 = QtWidgets.QComboBox(deadline_form)
        self.comboBox_2.setObjectName("comboBox_2")
        self.gridLayout.addWidget(self.comboBox_2, 2, 1, 1, 1)
        self.comboBox_8 = QtWidgets.QComboBox(deadline_form)
        self.comboBox_8.setObjectName("comboBox_8")
        self.gridLayout.addWidget(self.comboBox_8, 2, 7, 1, 1)
        self.comboBox_1 = QtWidgets.QComboBox(deadline_form)
        self.comboBox_1.setObjectName("comboBox_1")
        self.gridLayout.addWidget(self.comboBox_1, 2, 0, 1, 1)
        self.comboBox_6 = QtWidgets.QComboBox(deadline_form)
        self.comboBox_6.setObjectName("comboBox_6")
        self.gridLayout.addWidget(self.comboBox_6, 2, 5, 1, 1)
        self.comboBox_3 = QtWidgets.QComboBox(deadline_form)
        self.comboBox_3.setObjectName("comboBox_3")
        self.gridLayout.addWidget(self.comboBox_3, 2, 2, 1, 1)
        self.done_button = QtWidgets.QPushButton(deadline_form)
        self.done_button.setObjectName("done_button")
        self.gridLayout.addWidget(self.done_button, 1, 9, 1, 1)

        self.retranslateUi(deadline_form)
        QtCore.QMetaObject.connectSlotsByName(deadline_form)

    def retranslateUi(self, deadline_form):
        _translate = QtCore.QCoreApplication.translate
        deadline_form.setWindowTitle(
            _translate("deadline_form", "Task Deadline"))
        self.label.setText(_translate("deadline_form", "<html><head/><body><p align=\"center\">You know, I\'ve been thinking. Did you know that according to the Oxford English Dictionary, in the early days the word <span style=\" font-style:italic;\">deadline</span> just referred to lines that do not move?</p><p align=\"center\">Another line that does not move is the <span style=\" font-style:italic;\">International Date Line</span>, which it\'s amusing because people often misspell the word <span style=\" font-style:italic;\">deadline</span> as <span style=\" font-style:italic;\">dateline</span>.</p><p align=\"center\">Anyways, I find your usage of timezones and dates very <span style=\" font-weight:600;\">confusing</span>. My version is <span style=\" font-style:italic;\">far superior</span> so that\'s what you\'ll be using.</p><p align=\"center\">Please enter your intended task deadline in <span style=\" font-style:italic;\">UNIX time</span>.</p></body></html>"))
        self.done_button.setText(_translate("deadline_form", "Done"))

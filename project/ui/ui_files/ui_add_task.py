# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_add_task.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets


class Ui_task_form(object):
    def setupUi(self, task_form):
        task_form.setObjectName("task_form")
        task_form.resize(647, 452)
        self.form_title_button = QtWidgets.QPushButton(task_form)
        self.form_title_button.setGeometry(QtCore.QRect(9, 104, 120, 25))
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.form_title_button.sizePolicy().hasHeightForWidth())
        self.form_title_button.setSizePolicy(sizePolicy)
        self.form_title_button.setObjectName("form_title_button")
        self.form_desc_button = QtWidgets.QPushButton(task_form)
        self.form_desc_button.setGeometry(QtCore.QRect(390, 120, 120, 25))
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.form_desc_button.sizePolicy().hasHeightForWidth())
        self.form_desc_button.setSizePolicy(sizePolicy)
        self.form_desc_button.setObjectName("form_desc_button")
        self.form_date_button = QtWidgets.QPushButton(task_form)
        self.form_date_button.setGeometry(QtCore.QRect(180, 140, 120, 25))
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.form_date_button.sizePolicy().hasHeightForWidth())
        self.form_date_button.setSizePolicy(sizePolicy)
        self.form_date_button.setObjectName("form_date_button")
        self.form_done_button = QtWidgets.QPushButton(task_form)
        self.form_done_button.setGeometry(QtCore.QRect(9, 167, 120, 25))
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.form_done_button.sizePolicy().hasHeightForWidth())
        self.form_done_button.setSizePolicy(sizePolicy)
        self.form_done_button.setObjectName("form_done_button")
        self.label = QtWidgets.QLabel(task_form)
        self.label.setGeometry(QtCore.QRect(0, 0, 650, 70))
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label.setFont(font)
        self.label.setLineWidth(1)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setWordWrap(False)
        self.label.setObjectName("label")

        self.retranslateUi(task_form)
        QtCore.QMetaObject.connectSlotsByName(task_form)

    def retranslateUi(self, task_form):
        _translate = QtCore.QCoreApplication.translate
        task_form.setWindowTitle(_translate("task_form", "Create New Task"))
        self.form_title_button.setToolTip(_translate("task_form", "Add Title"))
        self.form_title_button.setText(_translate("task_form", "Done"))
        self.form_desc_button.setToolTip(
            _translate("task_form", "Add Description"))
        self.form_desc_button.setText(_translate("task_form", "Add Title"))
        self.form_date_button.setToolTip(
            _translate("task_form", "Add Deadline"))
        self.form_date_button.setText(
            _translate("task_form", "Add Description"))
        self.form_done_button.setToolTip(_translate("task_form", "Done"))
        self.form_done_button.setText(_translate("task_form", "Add Deadline"))
        self.label.setText(_translate("task_form", "<html><head/><body><p align=\"center\"><br/>oopsie whoopsie! I think I got the button names <span style=\" font-weight:600;\">mixed up</span>.</p><p align=\"center\"><span style=\" font-style:italic;\">look closely.</span></p></body></html>"))

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
        task_form.resize(400, 300)
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
        self.form_desc_button.setGeometry(QtCore.QRect(260, 50, 120, 25))
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

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_main.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets


class Ui_MainApplication(object):
    def setupUi(self, MainApplication):
        MainApplication.setObjectName("MainApplication")
        MainApplication.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainApplication)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.completed_button = QtWidgets.QPushButton(self.centralwidget)
        self.completed_button.setCheckable(False)
        self.completed_button.setObjectName("completed_button")
        self.gridLayout.addWidget(self.completed_button, 0, 2, 1, 1)
        self.remove_task_button = QtWidgets.QPushButton(self.centralwidget)
        self.remove_task_button.setObjectName("remove_task_button")
        self.gridLayout.addWidget(self.remove_task_button, 0, 1, 1, 1)
        self.create_task_button = QtWidgets.QPushButton(self.centralwidget)
        self.create_task_button.setObjectName("create_task_button")
        self.gridLayout.addWidget(self.create_task_button, 0, 0, 1, 1)
        self.edit_task_button = QtWidgets.QPushButton(self.centralwidget)
        self.edit_task_button.setCheckable(False)
        self.edit_task_button.setAutoDefault(False)
        self.edit_task_button.setFlat(False)
        self.edit_task_button.setObjectName("edit_task_button")
        self.gridLayout.addWidget(self.edit_task_button, 0, 3, 1, 1)
        self.task_table = QtWidgets.QTableView(self.centralwidget)
        self.task_table.setObjectName("task_table")
        self.gridLayout.addWidget(self.task_table, 1, 0, 1, 4)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        MainApplication.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainApplication)
        QtCore.QMetaObject.connectSlotsByName(MainApplication)

    def retranslateUi(self, MainApplication):
        _translate = QtCore.QCoreApplication.translate
        MainApplication.setWindowTitle(_translate(
            "MainApplication", "#TODO: Application"))
        self.completed_button.setText(_translate(
            "MainApplication", "Mark as Complete"))
        self.remove_task_button.setText(
            _translate("MainApplication", "Remove Task"))
        self.create_task_button.setText(
            _translate("MainApplication", "Create New Task"))
        self.edit_task_button.setText(
            _translate("MainApplication", "Edit Task"))

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_add_desc.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets


class Ui_desc_form(object):
    def setupUi(self, desc_form):
        desc_form.setObjectName("desc_form")
        desc_form.resize(600, 500)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(desc_form)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_2 = QtWidgets.QLabel(desc_form)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.label = QtWidgets.QLabel(desc_form)
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setKerning(True)
        self.label.setFont(font)
        self.label.setText("")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.reference_label = QtWidgets.QLabel(desc_form)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.reference_label.setFont(font)
        self.reference_label.setText("")
        self.reference_label.setAlignment(QtCore.Qt.AlignCenter)
        self.reference_label.setObjectName("reference_label")
        self.verticalLayout.addWidget(self.reference_label)
        self.done_button = QtWidgets.QPushButton(desc_form)
        self.done_button.setObjectName("done_button")
        self.verticalLayout.addWidget(self.done_button)
        self.text_slider = QtWidgets.QSlider(desc_form)
        self.text_slider.setMaximum(75)
        self.text_slider.setOrientation(QtCore.Qt.Horizontal)
        self.text_slider.setInvertedAppearance(False)
        self.text_slider.setInvertedControls(True)
        self.text_slider.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.text_slider.setTickInterval(5)
        self.text_slider.setObjectName("text_slider")
        self.verticalLayout.addWidget(self.text_slider)
        self.delete_button = QtWidgets.QPushButton(desc_form)
        self.delete_button.setObjectName("delete_button")
        self.verticalLayout.addWidget(self.delete_button)
        self.add_button = QtWidgets.QPushButton(desc_form)
        self.add_button.setObjectName("add_button")
        self.verticalLayout.addWidget(self.add_button)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(desc_form)
        QtCore.QMetaObject.connectSlotsByName(desc_form)

    def retranslateUi(self, desc_form):
        _translate = QtCore.QCoreApplication.translate
        desc_form.setWindowTitle(_translate("desc_form", "Task Description"))
        self.label_2.setText(_translate(
            "desc_form", "<html><head/><body><p align=\"center\">Enter the <span style=\" font-style:italic;\">description</span> of your task! The reference is still here so don\'t worry and <span style=\" font-weight:600;\">enjoy</span>!</p></body></html>"))
        self.done_button.setText(_translate("desc_form", "Done"))
        self.delete_button.setText(_translate("desc_form", "Delete Letter"))
        self.add_button.setText(_translate("desc_form", "Add Letter"))

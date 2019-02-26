# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_add_title.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets


class Ui_title_form(object):
    def setupUi(self, title_form):
        title_form.setObjectName("title_form")
        title_form.resize(400, 300)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(title_form)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(title_form)
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setKerning(True)
        self.label.setFont(font)
        self.label.setText("")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.add_button = QtWidgets.QPushButton(title_form)
        self.add_button.setObjectName("add_button")
        self.verticalLayout.addWidget(self.add_button)
        self.delete_button = QtWidgets.QPushButton(title_form)
        self.delete_button.setObjectName("delete_button")
        self.verticalLayout.addWidget(self.delete_button)
        self.text_slider = QtWidgets.QSlider(title_form)
        self.text_slider.setMaximum(75)
        self.text_slider.setOrientation(QtCore.Qt.Horizontal)
        self.text_slider.setInvertedAppearance(True)
        self.text_slider.setInvertedControls(False)
        self.text_slider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.text_slider.setTickInterval(5)
        self.text_slider.setObjectName("text_slider")
        self.verticalLayout.addWidget(self.text_slider)
        self.done_button = QtWidgets.QPushButton(title_form)
        self.done_button.setObjectName("done_button")
        self.verticalLayout.addWidget(self.done_button)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(title_form)
        QtCore.QMetaObject.connectSlotsByName(title_form)

    def retranslateUi(self, title_form):
        _translate = QtCore.QCoreApplication.translate
        title_form.setWindowTitle(_translate("title_form", "Task Title"))
        self.add_button.setText(_translate("title_form", "Add Letter"))
        self.delete_button.setText(_translate("title_form", "Delete Letter"))
        self.done_button.setText(_translate("title_form", "Done"))

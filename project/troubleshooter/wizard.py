# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'temp2.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_WizardPage1(object):
    def setupUi(self, WizardPage):
        WizardPage.setObjectName("WizardPage")
        WizardPage.resize(450, 300)
        self.horizontalLayout = QtWidgets.QHBoxLayout(WizardPage)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(WizardPage)
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)

        self.retranslateUi(WizardPage)
        QtCore.QMetaObject.connectSlotsByName(WizardPage)

    def retranslateUi(self, WizardPage):
        _translate = QtCore.QCoreApplication.translate
        WizardPage.setWindowTitle(_translate("WizardPage", "WizardPage"))
        self.label.setText(_translate("WizardPage", "Welcome to the Crocpad++ troubleshooter! Let me try and troubleshoot your problems."))

class Ui_Wizard(object):
    def setupUi(self, Wizard, pages):
        Wizard.setObjectName("Wizard")
        Wizard.resize(400, 290)

        pageNum = 0
        for page in pages:
            pageNum = pageNum + 1
            pageName = "page"+str(pageNum)
            page.setObjectName(pageName)
            Wizard.addPage(page)

        self.FinishButton.clicked.connect(self.close)
        self.CancelButton.clicked.connect(self.close)
        self.retranslateUi(Wizard)
        QtCore.QMetaObject.connectSlotsByName(Wizard)

    def retranslateUi(self, Wizard):
        _translate = QtCore.QCoreApplication.translate
        Wizard.setWindowTitle(_translate("Wizard", "Wizard"))


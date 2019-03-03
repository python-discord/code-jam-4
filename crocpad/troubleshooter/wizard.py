from PyQt5 import QtCore, QtGui, QtWidgets
from pathlib import Path
from threading import Thread
import time

class LoadingPage(object):
    def setupUi(self, WizardPage):
        WizardPage.setObjectName("WizardPage")
        WizardPage.resize(400, 300)
        WizardPage.setCommitPage(True)
        self.verticalLayoutWidget = QtWidgets.QWidget(WizardPage)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 381, 281))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.progressBar = QtWidgets.QProgressBar(self.verticalLayoutWidget)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout.addWidget(self.progressBar)
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        self.label.setFont(font)
        self.label.setCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.retranslateUi(WizardPage)
        QtCore.QMetaObject.connectSlotsByName(WizardPage)

    def retranslateUi(self, WizardPage):
        _translate = QtCore.QCoreApplication.translate
        WizardPage.setWindowTitle(_translate("WizardPage", "WizardPage"))
        self.label.setText(_translate("WizardPage", "loading troubleshooter..."))

class Ui_Wizard(object):
    def setupUi(self, Wizard):
        Wizard.setObjectName("Wizard")
        Wizard.resize(402, 300)
        icon = QtGui.QIcon()
        window_icon = str(Path('crocpad') / Path('crocpad.ico'))
        icon.addPixmap(QtGui.QPixmap(window_icon), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Wizard.setWindowIcon(icon)
        Wizard.setWizardStyle(QtWidgets.QWizard.ModernStyle)
        Wizard.setOptions(QtWidgets.QWizard.NoBackButtonOnStartPage)
        Wizard.setPixmap(QtWidgets.QWizard.LogoPixmap,
            QtGui.QPixmap(window_icon))

        self.help_button = Wizard.HelpButton
        self.stretch = Wizard.Stretch
        self.cancel_button = Wizard.CancelButton
        self.next_button = Wizard.NextButton
        self.finish_button = Wizard.FinishButton
        buttons = [self.help_button, self.stretch, self.cancel_button, self.next_button, self.finish_button]
        
        self.setButtonLayout(buttons)

        Wizard.button(self.help_button).clicked.connect(self.help)

        self.wizardPage1 = QtWidgets.QWizardPage()
        self.wizardPage1.setObjectName("wizardPage1")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.wizardPage1)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 391, 251))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        Wizard.addPage(self.wizardPage1)

        self.loadingPage = QtWidgets.QWizardPage()
        self.progressBar = LoadingPage().setupUi(self.loadingPage)
        self.loadingPage.setObjectName("loadingPage")
        Wizard.addPage(self.loadingPage)

        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        self.label.setFont(font)
        self.retranslateUi(Wizard)
        QtCore.QMetaObject.connectSlotsByName(Wizard)

    def retranslateUi(self, Wizard):
        Wizard.setWindowTitle(QtWidgets.QApplication.translate("Wizard", "crocpad++ troubleshooter", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("Wizard", "hello welcome to the crocpad++ troubleshooter let me fix ur problems", None, -1))
    
    def help(self):
        QtWidgets.QMessageBox.question(self, 'Help', "This is a troubleshooter.")

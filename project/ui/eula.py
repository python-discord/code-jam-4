from PyQt5 import QtCore, QtWidgets


class Ui_EulaDialog(object):
    def setupUi(self, EulaDialog):
        EulaDialog.setObjectName("EulaDialog")
        EulaDialog.resize(218, 701)
        self.clicked_button = None
        self.eula_TextEdit = QtWidgets.QPlainTextEdit(EulaDialog)
        self.eula_TextEdit.setGeometry(QtCore.QRect(10, 10, 201, 651))
        self.eula_TextEdit.setPlainText("")
        self.eula_TextEdit.setTextInteractionFlags(
            QtCore.Qt.TextSelectableByKeyboard | QtCore.Qt.TextSelectableByMouse)
        self.eula_TextEdit.setObjectName("eula_TextEdit")
        self.eula_disagree_button = QtWidgets.QPushButton(EulaDialog)
        self.eula_disagree_button.setGeometry(QtCore.QRect(10, 670, 61, 23))
        self.eula_disagree_button.setObjectName("eula_disagree_button")
        self.eula_agree_button = QtWidgets.QPushButton(EulaDialog)
        self.eula_agree_button.setGeometry(QtCore.QRect(80, 670, 131, 23))
        self.eula_agree_button.setObjectName("eula_agree_button")
        self.eula_agree_button.clicked.connect(self.clickedButton)

        self.retranslateUi(EulaDialog)
        QtCore.QMetaObject.connectSlotsByName(EulaDialog)

    def clickedButton(self):
        self.clicked_button = self.eula_agree_button
        self.close()

    def retranslateUi(self, EulaDialog):
        _translate = QtCore.QCoreApplication.translate
        EulaDialog.setWindowTitle(_translate("EulaDialog", "License"))
        self.eula_disagree_button.setText(_translate("EulaDialog", "Disagree"))
        self.eula_agree_button.setText(_translate("EulaDialog", "Reconfirm Agreement"))

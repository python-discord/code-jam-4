from PyQt5 import QtCore, QtWidgets


class Editor(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(463, 258)
        Dialog.setMinimumSize(QtCore.QSize(463, 258))
        Dialog.setMaximumSize(QtCore.QSize(463, 258))
        self.save_button = QtWidgets.QPushButton(Dialog)
        self.save_button.setGeometry(QtCore.QRect(150, 230, 75, 21))
        self.save_button.setObjectName("pushButton")
        self.save_button.clicked.connect(self.save)
        self.cancel_button = QtWidgets.QPushButton(Dialog)
        self.cancel_button.setGeometry(QtCore.QRect(230, 230, 75, 21))
        self.cancel_button.setObjectName("pushButton_2")
        self.cancel_button.clicked.connect(self.cancel)
        self.textEdit = QtWidgets.QTextEdit(Dialog)
        self.textEdit.setGeometry(QtCore.QRect(0, 0, 461, 221))
        self.textEdit.setObjectName("textEdit")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.save_button.setText(_translate("Dialog", "Save"))
        self.cancel_button.setText(_translate("Dialog", "Cancel"))

    def save(self):
        print(self.textEdit.toPlainText())

    def cancel(self):
        sys.exit(app.exec_())


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Editor()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

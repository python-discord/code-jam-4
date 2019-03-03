import random
from PySide2 import QtCore, QtWidgets


class MyWidget(QtWidgets.QWidget):
    count = 0

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle("Edit Task")
        self.resize(300, 200)

        self.greetings = [
            "Are you sure you wanna edit?",
            "It is weird that you want to edit.",
            "Why do you want to edit?",
            "I do not think that is a wise choice",
            "Beep! Beep! Wrong choice!"
        ]

        self.button = QtWidgets.QPushButton("Click to edit")
        self.text = QtWidgets.QLabel("Edit Task?")
        self.text.setAlignment(QtCore.Qt.AlignCenter)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)

        self.button.clicked.connect(self.magic)

    def magic(self):
        if MyWidget.count < 5:
            self.text.setText(random.choice(self.greetings))
            MyWidget.count += 1
        else:
            self.text = QtWidgets.QLabel("Sorry! Wrong Answer! Function is disabled..")
            self.button.setEnabled(False)
            self.button.setDisabled(True)

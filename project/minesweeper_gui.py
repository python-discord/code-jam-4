from PyQt5 import QtWidgets
from itertools import product
from functools import partial
import sys

class Minesweeper(QtWidgets.QWidget):
    """Minesweeper Game Widget"""

    def __init__(self, width=16, height=16, parent=None):
        super().__init__(parent)
        self.width = width
        self.height = height
        self.setup_gui()

    def setup_gui(self):
        """Setup the GUI for the minesweeper widget"""
        layout = QtWidgets.QGridLayout(self)
        layout.setSpacing(0)

        for row, column in product(range(self.height), range(self.width)):
            button = QtWidgets.QPushButton()
            button.clicked.connect(partial(self.button_clicked, row, column))
            button.setFixedSize(30, 30)
            layout.addWidget(button, row, column)

        self.setLayout(layout)

    def button_clicked(self, row, column):
        print("Button Clicked", row, column)


if __name__ == '__main__':
    # create the PyQt5 app
    app = QtWidgets.QApplication(sys.argv)

    window = Minesweeper(width=16, height=16)
    window.show()

    sys.exit(app.exec_())

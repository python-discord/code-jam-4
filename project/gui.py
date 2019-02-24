from PyQt5 import QtWidgets, QtCore, QtGui
from functools import partial
from . import logic
import sys
import os

BASE_DIR = os.path.dirname(__file__)

class Tile(QtWidgets.QPushButton):
    '''Represents a Tile on a minesweeper grid'''

    right_clicked = QtCore.pyqtSignal()

    def mousePressEvent(self, event):
        if event.buttons() == QtCore.Qt.RightButton:
            self.right_clicked.emit()
        else:
            super().mousePressEvent(event)


class Minesweeper(QtWidgets.QWidget):
    '''Minesweeper Game Widget'''

    def __init__(self, width=16, height=16, parent=None):
        super().__init__(parent)
        self.width = width
        self.height = height
        self.controller = logic.Minesweeper(self.width, self.height)
        self.controller.put_mines_in_grid(20)
        self.button_grid = []
        self.setup_gui()

    def setup_gui(self):
        '''Setup the GUI for the minesweeper widget'''
        self.grid_layout = QtWidgets.QGridLayout(self)
        self.grid_layout.setSpacing(0)

        for row in range(self.width):
            row_array = []
            for column in range(self.height):
                button = Tile()
                button.clicked.connect(partial(self.button_clicked, row, column))
                button.right_clicked.connect(partial(self.place_flag, row, column))
                button.setFixedSize(30, 30)
                self.grid_layout.addWidget(button, row, column)
                row_array.append(button)
            self.button_grid.append(row_array)

        self.setLayout(self.grid_layout)

    def refresh_gui(self):
        '''Refresh the GUI to match the same grid on the minesweeper controller'''
        for y, row in enumerate(self.controller.grid):
            for x, tile in enumerate(row):
                if tile == self.controller.DISCOVERED:
                    self.button_grid[y][x].hide()
                    number = self.controller.get_tile_number(x, y)
                    if number:
                        label = QtWidgets.QLabel(str(number))
                        self.grid_layout.addWidget(label, y, x)

    def place_flag(self, row, column):
        button = self.button_grid[row][column]
        icon = QtGui.QIcon(':/images/flag.png')
        if not button.icon().isNull():
           button.setIcon(QtGui.QIcon())
        else:
            button.setIcon(icon)
            

    def button_clicked(self, row, column):
        self.controller.click_tile(x=column, y=row)
        self.refresh_gui()


if __name__ == '__main__':
    # create the PyQt5 app
    app = QtWidgets.QApplication(sys.argv)

    window = Minesweeper(width=16, height=16)
    window.show()

    sys.exit(app.exec_())

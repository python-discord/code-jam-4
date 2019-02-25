from PyQt5 import QtWidgets, QtCore, QtGui
from functools import partial
from . import logic
import os
import sys


class Tile(QtWidgets.QPushButton):
    '''Represents a Tile on a minesweeper grid'''

    right_clicked = QtCore.pyqtSignal()
    health_decreased = QtCore.pyqtSignal()

    def __init__(self, health, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setObjectName('tile')
        self.max_health = health  # this refers to the amount of clicks it takes to destroy
        self.health = health

    def health_percent(self):
        return int((self.health / self.max_health)*100)

    def mousePressEvent(self, event):
        if event.buttons() == QtCore.Qt.RightButton:
            self.right_clicked.emit()
        elif event.buttons() == QtCore.Qt.LeftButton and self.health > 1:
            self.health -= 1
            self.health_decreased.emit()
        else:
            super().mousePressEvent(event)


class Minesweeper(QtWidgets.QWidget):
    '''Minesweeper Game Widget'''

    def __init__(self, width=16, height=16, parent=None):
        super().__init__(parent)
        self.setObjectName('minesweeper')
        self.width = width
        self.height = height
        self.tile_size = (25, 25)
        self.controller = logic.Minesweeper(self.width, self.height)
        self.controller.put_mines_in_grid(10)
        self.button_grid = []
        self.setup_gui()

    def load_css(self):
        css_file = os.path.join(os.path.dirname(__file__), 'theme.css')
        with open(css_file) as file:
            self.setStyleSheet(file.read())

    def setup_gui(self):
        '''Setup the GUI for the minesweeper widget'''
        self.load_css()
        self.grid_layout = QtWidgets.QGridLayout(self)
        self.grid_layout.setSpacing(0)

        for row in range(self.width):
            row_array = []
            for column in range(self.height):
                button = Tile(10)
                button.clicked.connect(partial(self.button_clicked, row, column))
                button.right_clicked.connect(partial(self.place_flag, row, column))
                button.health_decreased.connect(partial(self.button_health_update, row, column))
                button.setFixedSize(*self.tile_size)
                self.grid_layout.addWidget(button, row, column)
                row_array.append(button)
            self.button_grid.append(row_array)

        self.setLayout(self.grid_layout)

    def button_health_update(self, row, column):
        '''Updates the button whenever the health has changed'''
        button = self.button_grid[row][column]
        current_index = 9 - (button.health_percent() // 10)
        button.setStyleSheet(f'background-image: url(:/tiles/crack{current_index}.png);'
                             f'background-position: center;')

    def refresh_gui(self):
        '''Refresh the GUI to match the same grid on the minesweeper controller'''
        for y, row in enumerate(self.controller.grid):
            for x, tile in enumerate(row):
                if tile == self.controller.DISCOVERED:
                    self.button_grid[y][x].hide()
                    number = self.controller.get_tile_number(x, y)
                    if number:
                        colours = {'1': QtGui.QColor(0x0000FF),
                                   '2': QtGui.QColor(0x00FF00),
                                   '3': QtGui.QColor(0xFF0000),
                                   '4': QtGui.QColor(0x0000FF).darker(100),
                                   '5': QtGui.QColor(0x00FF00).darker(100),
                                   '6': QtGui.QColor(0xFF0000).darker(100),
                                   '7': QtGui.QColor(0x0000FF).darker(200),
                                   '8': QtGui.QColor(0x00FF00).darker(200)}
                        font = QtGui.QFont('Consolas')
                        font.setBold(True)
                        label = QtWidgets.QLabel(str(number))
                        label.setStyleSheet('color: ' + colours[str(number)].name())
                        label.setFont(font)
                        label.setAlignment(QtCore.Qt.AlignCenter)
                        label.setFixedSize(*self.tile_size)
                        self.grid_layout.addWidget(label, y, x)

    def place_flag(self, row, column):
        button = self.button_grid[row][column]
        flag_icon = QtGui.QIcon(':/images/flag.png')
        if not button.icon().isNull():
            button.setIcon(QtGui.QIcon())
        else:
            button.setIcon(flag_icon)

    def game_over(self):
        for y, row in enumerate(self.controller.grid):
            for x, tile in enumerate(row):
                if tile == self.controller.MINE:
                    self.button_grid[y][x].hide()
                    label = QtWidgets.QLabel(self)
                    label.setFixedSize(*self.tile_size)
                    size = label.size()
                    mine_icon = QtGui.QPixmap(':/images/mine.png')
                    scaled_mine_icon = mine_icon.scaled(
                        size,
                        QtCore.Qt.KeepAspectRatio,
                        transformMode=QtCore.Qt.SmoothTransformation)
                    label.setPixmap(scaled_mine_icon)
                    self.grid_layout.addWidget(label, y, x)

    def button_clicked(self, row, column):
        is_mine = self.controller.click_tile(x=column, y=row)
        if is_mine:
            self.game_over()
        self.refresh_gui()


if __name__ == '__main__':
    # create the PyQt5 app
    app = QtWidgets.QApplication(sys.argv)

    window = Minesweeper(width=16, height=16)
    window.show()

    sys.exit(app.exec_())

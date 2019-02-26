from PyQt5 import QtWidgets, QtCore, QtGui, QtMultimedia
from functools import partial
from . import logic
import time
import random
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
        self.setFlat(False)

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


class MinesweeperModal(QtWidgets.QFrame):
    '''Minesweeper Modal Widget'''

    def __init__(self, message, parent):
        super().__init__(parent)
        self.setObjectName('modal')
        self.setFixedSize(300, 100)
        self.message = message
        self.setHidden(True)
        self.setup_gui()

    def setup_gui(self):
        self.v_layout = QtWidgets.QVBoxLayout(self)
        self.v_layout.setContentsMargins(15, 20, 15, 20)
        self.v_layout.setSpacing(5)
        self.v_layout.setAlignment(QtCore.Qt.AlignHCenter)

        font = QtGui.QFont('Consolas')
        font.setPointSize(12)
        self.title_label = QtWidgets.QLabel(self.message)
        self.title_label.setFont(font)

        self.close_button = QtWidgets.QPushButton("OK")
        self.close_button.setSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                        QtWidgets.QSizePolicy.Preferred)
        self.close_button.setFont(font)

        self.v_layout.addWidget(self.title_label)
        self.v_layout.addWidget(self.close_button)
        self.setLayout(self.v_layout)


class Minesweeper(QtWidgets.QWidget):
    '''Minesweeper Game Widget'''

    game_over = QtCore.pyqtSignal()

    def __init__(self, width=16, height=16, mines=48, parent=None):
        super().__init__(parent)
        self.setObjectName('minesweeper')
        self.last_click = 0
        self.grid_width = width
        self.grid_height = height
        self.explosion_sound = QtMultimedia.QSound(':/sound/explode.wav')
        self.beep_sound = QtMultimedia.QSound(':/sound/beep.wav')
        self.break_sound = QtMultimedia.QSound(':/sound/break.wav')
        self.tile_size = (20, 20)
        self.controller = logic.Minesweeper(self.grid_width, self.grid_height)
        self.controller.mines_number = mines
        self.button_grid = []
        self.setup_gui()

    def show_click_modal(self):
        '''Shows a floating modal widget in the center of the screen which tells you
        to stop clicking so fast'''
        self.beep_sound.play()
        self.too_fast_modal.setHidden(False)
        self.too_fast_modal.raise_()
        self.game_frame.setDisabled(True)

    def modal_closed(self):
        '''This action is called when a modal is closed'''
        self.too_fast_modal.setHidden(True)
        self.game_frame.setDisabled(False)

    def load_css(self):
        '''Loads a CSS file and loads it into the Minesweeper widget'''
        css_file = os.path.join(os.path.dirname(__file__), 'theme.css')
        with open(css_file) as file:
            self.setStyleSheet(file.read())

    def setup_gui(self):
        '''Setup the GUI for the minesweeper widget'''
        self.load_css()
        self.window_layout = QtWidgets.QVBoxLayout(self)
        self.game_frame = QtWidgets.QFrame(self)
        self.grid_layout = QtWidgets.QGridLayout(self.game_frame)
        self.grid_layout.setSpacing(1)

        for row in range(self.grid_height):
            row_array = []
            for column in range(self.grid_width):
                button = Tile(random.randint(30, 100))
                button.clicked.connect(partial(self.button_clicked, row, column))
                button.right_clicked.connect(partial(self.place_flag, row, column))
                button.health_decreased.connect(partial(self.button_health_update, row, column))
                button.setFixedSize(*self.tile_size)
                self.grid_layout.addWidget(button, row, column)
                row_array.append(button)
            self.button_grid.append(row_array)

        self.game_frame.setLayout(self.grid_layout)
        self.window_layout.addWidget(self.game_frame)
        self.setLayout(self.window_layout)

        self.show()

        # Floating Modal
        self.too_fast_modal = MinesweeperModal('You are clicking too fast!', self)
        self.too_fast_modal.close_button.clicked.connect(self.modal_closed)
        self.too_fast_modal.move(self.rect().center()-self.too_fast_modal.rect().center())

    def refresh_gui(self):
        '''Refresh the GUI to match the same grid on the minesweeper controller'''
        for y, row in enumerate(self.controller.grid):
            for x, tile in enumerate(row):
                if tile == self.controller.DISCOVERED:
                    self.button_grid[y][x].hide()
                    number = self.controller.get_tile_number(x, y)
                    label = QtWidgets.QLabel()
                    label.setFixedSize(*self.tile_size)
                    if number:
                        colours = {'1': QtGui.QColor(0x76a4ed),
                                   '2': QtGui.QColor(0x77ed76),
                                   '3': QtGui.QColor(0xed7676),
                                   '4': QtGui.QColor(0xedab76),
                                   '5': QtGui.QColor(0x76edd9),
                                   '6': QtGui.QColor(0xb576ed),
                                   '7': QtGui.QColor(0x767bed),
                                   '8': QtGui.QColor(0xed76d5)}
                        font = QtGui.QFont('Consolas')
                        label.setText(str(number))
                        label.setStyleSheet('color: ' + colours[str(number)].name())
                        label.setFont(font)
                        label.setAlignment(QtCore.Qt.AlignCenter)
                    self.grid_layout.addWidget(label, y, x)

    def place_flag(self, row, column):
        '''Toggles the flag showing feature on a tile'''
        button = self.button_grid[row][column]
        flag_icon = QtGui.QIcon(':/images/flag.png')
        if not button.icon().isNull():
            button.setIcon(QtGui.QIcon())
        else:
            button.setIcon(flag_icon)

    def explode(self, row, column):
        '''Explodes the specified tile, with a sound effect and a GIF'''
        self.button_grid[row][column].hide()
        explode_label = QtWidgets.QLabel()
        explosion = QtGui.QMovie(':/images/explosion.gif')
        explosion.setScaledSize(QtCore.QSize(*self.tile_size))
        explosion.start()
        explosion.frameChanged.connect(partial(self.explode_frame_count, explode_label,
                                               explosion.frameCount()))
        explode_label.setMovie(explosion)
        explode_label.setAlignment(QtCore.Qt.AlignCenter)
        self.grid_layout.addWidget(explode_label, row, column)
        self.explosion_sound.play()

    def explode_frame_count(self, label, max_frames, current_frame):
        '''This event is called when the frame on the explosion GIF updates, it is to make sure that
        the GIF stops and is replaced with a mine PNG after it has reached its max frame'''
        if current_frame == max_frames-1:
            mine_icon = QtGui.QPixmap(':/images/mine.png')
            scaled_mine_icon = mine_icon.scaled(*self.tile_size)
            label.setPixmap(scaled_mine_icon)

    def explode_all_mines(self, row, column):
        '''Call this function to explode all mines'''
        self.explode_all_mines_thread = DelayMineExplosionThread(self, first=(column, row))
        self.explode_all_mines_thread.finished.connect(self.game_over.emit)
        self.explode_all_mines_thread.explode.connect(self.explode)
        self.explode_all_mines_thread.start()

    def button_health_update(self, row, column):
        '''Updates the button whenever the health has changed'''

        # Stops you from clicking too fast
        click_time = time.time()
        if click_time - self.last_click <= 0.2:
            self.show_click_modal()
        self.last_click = time.time()

        button = self.button_grid[row][column]
        current_index = 9 - (button.health_percent() // 10)
        button.setStyleSheet(f'background-image: url(:/tiles/crack{current_index}.png);'
                             f'background-position: center;')

    def button_clicked(self, row, column):
        '''This is called when a button is clicked at the position (row, column)'''
        mine = self.controller.click_tile(x=column, y=row)
        if not mine:
            self.refresh_gui()
            self.break_sound.play()
        else:
            self.break_sound.play()
            self.explode_all_mines(row, column)


class DelayMineExplosionThread(QtCore.QThread):
    '''Creates a shuffled, random and delayed 'emission' of signals
    Used for creating random explosions of all mines at game over'''

    finished = QtCore.pyqtSignal()
    explode = QtCore.pyqtSignal(int, int)

    def __init__(self, minesweeper, first):
        self.positions = list(minesweeper.controller.mine_positions)
        self.first = first
        super().__init__()

    def run(self):
        '''Shuffles and emits the signals for exploding'''
        random.shuffle(self.positions)
        self.positions.remove(self.first)
        self.positions.insert(0, self.first)
        bomb_number = len(self.positions)
        for column, row in self.positions:
            self.explode.emit(row, column)
            time.sleep(abs((1/bomb_number)+(random.random()-0.5)/10))
        self.finished.emit()


if __name__ == '__main__':
    # create the PyQt5 app
    app = QtWidgets.QApplication(sys.argv)

    window = Minesweeper(width=16, height=16)
    window.show()
    window.setFixedSize(window.minimumSize())

    sys.exit(app.exec_())

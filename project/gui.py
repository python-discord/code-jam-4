from PyQt5 import QtWidgets, QtCore, QtGui, QtMultimedia
from functools import partial
from itertools import count
from . import logic
import time
import random
import os


class MinesweeperApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Minesweeper')
        self.setWindowIcon(QtGui.QIcon(':/images/mine.png'))
        self.setup_ui()

    def setup_ui(self):
        '''Setup UI for main application'''
        self.stack_widget = QtWidgets.QStackedWidget()

        # Main Menu Widget
        self.home_screen = MenuWidget()
        self.home_screen.start_button.clicked.connect(self.start_game)
        self.stack_widget.addWidget(self.home_screen)

        self.setCentralWidget(self.stack_widget)
        self.load_css()

    def load_css(self):
        '''Loads a CSS file and loads it into the Minesweeper widget'''
        css_file = os.path.join(os.path.dirname(__file__), 'theme.css')
        with open(css_file) as file:
            self.setStyleSheet(file.read())

    def start_game(self):
        # Minesweeper Widget
        width = int(self.home_screen.set_width_input.text())
        height = int(self.home_screen.set_height_input.text())
        mines = int(self.home_screen.set_mines_input.text())
        if width * height <= mines:
            QtWidgets.QMessageBox.warning(self, 'Too many mines',
                                          'The amount of mines you entered is too big for the grid')
            return
        self.minesweeper = Minesweeper(width, height, mines)
        self.minesweeper.setup_gui()
        self.stack_widget.addWidget(self.minesweeper)
        self.stack_widget.setCurrentWidget(self.minesweeper)


# Home Screen Widget


class MenuWidget(QtWidgets.QWidget):
    '''Main Menu Widget (Home Screen)'''

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_gui()

    def setup_gui(self):
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(96, 32, 96, 32)
        layout.setSpacing(32)
        layout.setAlignment(QtCore.Qt.AlignHCenter)
        form_layout = QtWidgets.QFormLayout()

        font = QtGui.QFont('Consolas')
        font.setPointSize(14)
        title_label = QtWidgets.QLabel('Minesweeper Game')
        title_label.setFont(font)
        title_label.setObjectName("title")
        font.setPointSize(10)
        width_label = QtWidgets.QLabel('Grid Width: ')
        width_label.setFont(font)
        height_label = QtWidgets.QLabel('Grid Height: ')
        height_label.setFont(font)
        mines_label = QtWidgets.QLabel('No. of Mines: ')
        mines_label.setFont(font)

        self.onlyInt = QtGui.QIntValidator()

        self.set_width_input = QtWidgets.QLineEdit('16')
        self.set_width_input.setMaxLength(2)
        self.set_width_input.setFixedWidth(30)
        self.set_width_input.setValidator(self.onlyInt)
        self.set_height_input = QtWidgets.QLineEdit('16')
        self.set_height_input.setMaxLength(2)
        self.set_height_input.setFixedWidth(30)
        self.set_height_input.setValidator(self.onlyInt)
        self.set_mines_input = QtWidgets.QLineEdit('64')
        self.set_mines_input.setMaxLength(3)
        self.set_mines_input.setFixedWidth(30)
        self.set_mines_input.setValidator(self.onlyInt)

        form_layout.addRow(width_label, self.set_width_input)
        form_layout.addRow(height_label, self.set_height_input)
        form_layout.addRow(mines_label, self.set_mines_input)
        form_layout.setFormAlignment(QtCore.Qt.AlignCenter)
        form_layout.setSpacing(5)

        self.start_button = QtWidgets.QPushButton('Start')
        self.start_button.setFont(font)
        self.start_button.setObjectName("menuButton")

        layout.addWidget(title_label)
        layout.setAlignment(title_label, QtCore.Qt.AlignCenter)
        layout.addLayout(form_layout)
        layout.addWidget(self.start_button)
        layout.setAlignment(self.start_button, QtCore.Qt.AlignCenter)
        self.setLayout(layout)


# Minesweeper Widgets

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

    def __str__(self):
        return f'[{self.health_percent()}]'

    def __repr__(self):
        return self.__str__()


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
        self.flag_count = mines
        self.too_fast_modal = None
        self.game_over_modal = None

    def setup_gui(self):
        '''Setup the GUI for the minesweeper widget'''
        self.window_layout = QtWidgets.QVBoxLayout(self)
        self.window_layout.setSpacing(0)
        self.window_layout.setContentsMargins(0, 0, 0, 0)

        # -- SCORE PANEL
        self.score_frame = QtWidgets.QFrame(self)
        self.score_frame.setObjectName('score')
        h_layout = QtWidgets.QHBoxLayout(self.score_frame)
        h_layout.setSpacing(10)
        flag_count_label = QtWidgets.QLabel('Flags')
        flag_count_label.setFont(QtGui.QFont('Consolas'))
        self.flag_count_lcd = QtWidgets.QLCDNumber(self.score_frame)
        self.flag_count_lcd.setSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                          QtWidgets.QSizePolicy.Fixed)
        self.flag_count_lcd.display(self.flag_count)
        self.flag_count_lcd.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        spacer = QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Expanding,
                                       QtWidgets.QSizePolicy.Preferred)
        timer_label = QtWidgets.QLabel('Time')
        timer_label.setFont(QtGui.QFont('Consolas'))
        self.timer_lcd = QtWidgets.QLCDNumber(self.score_frame)
        self.timer_lcd.setSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                     QtWidgets.QSizePolicy.Fixed)
        self.timer_lcd.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.counter_thread = TimerThread()
        self.counter_thread.update.connect(self.timer_lcd.display)
        self.counter_thread.start()

        self.score_frame.setLayout(h_layout)

        h_layout.addWidget(flag_count_label)
        h_layout.addWidget(self.flag_count_lcd)
        h_layout.addSpacerItem(spacer)
        h_layout.addWidget(timer_label)
        h_layout.addWidget(self.timer_lcd)

        # -- GAME PANEL
        self.game_frame = QtWidgets.QFrame(self)
        self.game_frame.setObjectName('game')
        self.grid_layout = QtWidgets.QGridLayout()
        self.grid_layout.setContentsMargins(48, 48, 48, 48)
        self.grid_layout.setSpacing(1)

        # Adding spacers around the grid so it doesn't spread out when resized
        horizontal_spacer = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Expanding,
                                                  QtWidgets.QSizePolicy.Fixed)
        vertical_spacer = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Fixed,
                                                QtWidgets.QSizePolicy.Expanding)
        self.grid_layout.addItem(horizontal_spacer, 1, 0, rowSpan=self.grid_height)
        self.grid_layout.addItem(horizontal_spacer, 1, self.grid_width+1, rowSpan=self.grid_width)
        self.grid_layout.addItem(vertical_spacer, 0, 1, columnSpan=self.grid_height)
        self.grid_layout.addItem(vertical_spacer, self.grid_height+1, 1, columnSpan=self.grid_width)

        # generating the grid of tiles
        # need a placeholder value to set offset so it matches with the grid layout, hence the None
        self.button_grid = [[None]]
        for row in range(1, self.grid_height+1):
            row_array = [None]
            for column in range(1, self.grid_width+1):
                button = Tile(random.randint(1, 1)) #TODO MAKE SURE THIS IS CHANGED TO A HIGH NUMBER
                button.clicked.connect(partial(self.button_clicked, row, column))
                button.right_clicked.connect(partial(self.place_flag, row, column))
                button.health_decreased.connect(partial(self.button_health_update, row, column))
                button.setFixedSize(*self.tile_size)
                self.grid_layout.addWidget(button, row, column)
                row_array.append(button)
            self.button_grid.append(row_array)

        self.game_frame.setLayout(self.grid_layout)
        self.window_layout.addWidget(self.game_frame)
        self.window_layout.addWidget(self.score_frame)
        self.setLayout(self.window_layout)

    def show_click_modal(self):
        '''Shows a floating modal widget in the center of the screen which tells you
        to stop clicking so fast'''

        if self.too_fast_modal is None:
            self.too_fast_modal = MinesweeperModal('You are clicking too fast!', self)
            self.too_fast_modal.close_button.clicked.connect(self.modal_closed)
            self.too_fast_modal.move(self.rect().center() - self.too_fast_modal.rect().center())

        self.beep_sound.play()
        self.too_fast_modal.setHidden(False)
        self.too_fast_modal.raise_()
        self.game_frame.setDisabled(True)

    def show_game_over_modal(self):
        '''Shows a game over modal in the center of the screen which takes you
        back to the main menu if you click ok'''

        if self.game_over_modal is None:
            self.game_over_modal = MinesweeperModal('GAME OVER', self)
            self.game_over_modal.close_button.clicked.connect(self.end_game)
            self.game_over_modal.move(self.rect().center() - self.game_over_modal.rect().center())

        self.beep_sound.play()
        self.game_over_modal.setHidden(False)
        self.game_over_modal.raise_()
        self.game_frame.setDisabled(True)

    def end_game(self):
        '''This event is called when the game ends'''
        pass

    def modal_closed(self):
        '''This action is called when a modal is closed'''
        self.game_over_modal.setHidden(True)
        self.too_fast_modal.setHidden(True)
        self.game_frame.setDisabled(False)

    def refresh_gui(self):
        '''Refresh the GUI to match the same grid on the minesweeper controller'''
        for y, row in enumerate(self.controller.grid):
            for x, tile in enumerate(row):
                if tile == self.controller.DISCOVERED:
                    self.button_grid[y+1][x+1].hide()
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
                    self.grid_layout.addWidget(label, y+1, x+1)

    def place_flag(self, row, column):
        '''Toggles the flag showing feature on a tile'''
        button = self.button_grid[row][column]
        flag_icon = QtGui.QIcon(':/images/flag.png')
        if not button.icon().isNull():
            self.flag_count += 1
            button.setIcon(QtGui.QIcon())
        elif self.flag_count > 0:
            self.flag_count -= 1
            button.setIcon(flag_icon)
            button.health = button.max_health
            button.setStyleSheet("")
        self.flag_count_lcd.display(self.flag_count)

    def explode(self, row, column):
        '''Explodes the specified tile, with a sound effect and a GIF'''
        self.button_grid[row+1][column+1].hide()
        explode_label = QtWidgets.QLabel()
        explosion = QtGui.QMovie(':/images/explosion.gif')
        explosion.setScaledSize(QtCore.QSize(*self.tile_size))
        explosion.start()
        explosion.frameChanged.connect(partial(self.explode_frame_count, explode_label,
                                               explosion.frameCount()))
        explode_label.setMovie(explosion)
        explode_label.setAlignment(QtCore.Qt.AlignCenter)
        self.grid_layout.addWidget(explode_label, row+1, column+1)
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
        self.explode_all_mines_thread = DelayMineExplosionThread(self, first=(column-1, row-1))
        self.explode_all_mines_thread.finished.connect(self.game_over.emit)
        self.explode_all_mines_thread.explode.connect(self.explode)
        self.explode_all_mines_thread.start()
        self.show_game_over_modal()

    def button_health_update(self, row, column):
        '''Updates the button whenever the health has changed'''

        # Stops you from clicking too fast
        click_time = time.time()
        if click_time - self.last_click <= 0.3:
            self.show_click_modal()
        self.last_click = time.time()

        button = self.button_grid[row][column]
        if not button.icon().isNull():
            self.place_flag(row, column)
        current_index = 9 - (button.health_percent() // 10)
        button.setStyleSheet(f'background-image: url(:/tiles/crack{current_index}.png);'
                             f'background-position: center;')

    def button_clicked(self, row, column):
        '''This is called when a button is clicked at the position (row, column)'''
        mine = self.controller.click_tile(x=column-1, y=row-1)
        if not mine:
            self.refresh_gui()
            self.break_sound.play()
        else:
            self.break_sound.play()
            self.explode_all_mines(row, column)


class TimerThread(QtCore.QThread):
    '''Simply counts upwards to infinity with a second delay'''

    update = QtCore.pyqtSignal(int)

    def run(self):
        for number in count(0):
            self.update.emit(number)
            time.sleep(1)


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
            time.sleep(abs((1/bomb_number)+(random.random()-0.5)/5))
        self.finished.emit()

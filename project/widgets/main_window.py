from PySide2.QtMultimedia import QMediaPlayer, QMediaPlaylist
from PySide2.QtWidgets import QMainWindow

from project.ui.main_window import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.player = QMediaPlayer()
        self.playlist = QMediaPlaylist()

        self.play_button.pressed.connect(self.player.play)
        self.previous_button.pressed.connect(self.playlist.previous)
        self.next_button.pressed.connect(self.playlist.next)

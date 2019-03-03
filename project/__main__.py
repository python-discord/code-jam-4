from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt, QUrl
from PyQt5 import QtMultimedia
from .gui import MinesweeperApp
from . import resources  # noqa
import sys
import os


if __name__ == '__main__':
    # For high DPI displays
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)

    app = QApplication(sys.argv)

    # This plays the background music in a continuous loop
    music_file = os.path.join(os.path.dirname(__file__), 'background.mp3')
    bgm_playlist = QtMultimedia.QMediaPlaylist()
    bgm_playlist.addMedia(QtMultimedia.QMediaContent(
        QUrl.fromLocalFile(music_file)))
    bgm_playlist.setPlaybackMode(QtMultimedia.QMediaPlaylist.Loop)
    bgm_player = QtMultimedia.QMediaPlayer()
    bgm_player.setPlaylist(bgm_playlist)
    bgm_player.play()

    window = MinesweeperApp()
    window.show()

    sys.exit(app.exec_())

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt, QUrl
from PyQt5 import QtMultimedia
from .gui import MinesweeperApp
from . import resources  # noqa
import sys

if __name__ == '__main__':
    # For high DPI displays
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)

    app = QApplication(sys.argv)

    bgmplaylist = QtMultimedia.QMediaPlaylist()
    bgmplaylist.addMedia(QtMultimedia.QMediaContent(
        QUrl.fromLocalFile("./project/resources/elevator.mp3")))
    bgmplaylist.setPlaybackMode(QtMultimedia.QMediaPlaylist.Loop)
    bgmplayer = QtMultimedia.QMediaPlayer()
    bgmplayer.setPlaylist(bgmplaylist)
    bgmplayer.play()

    window = MinesweeperApp()
    window.show()

    sys.exit(app.exec_())

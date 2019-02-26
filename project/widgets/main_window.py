import logging

from PySide2.QtCore import QUrl, Qt
from PySide2.QtMultimedia import QMediaContent, QMediaPlayer, QMediaPlaylist
from PySide2.QtSql import QSqlTableModel
from PySide2.QtWidgets import QAbstractItemView, QFileDialog, QMainWindow

from project import library, media as media_utils
from project.ui.main_window import Ui_MainWindow

log = logging.getLogger(__name__)


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.player = QMediaPlayer()
        self.playlist = QMediaPlaylist()

        self.library_model = QSqlTableModel()
        self.library_model.setTable("library")
        self.library_model.setHeaderData(1, Qt.Horizontal, "Title", Qt.DisplayRole)
        self.library_model.setHeaderData(2, Qt.Horizontal, "Artist", Qt.DisplayRole)
        self.library_model.setHeaderData(3, Qt.Horizontal, "Album", Qt.DisplayRole)
        self.library_model.setHeaderData(4, Qt.Horizontal, "Genre", Qt.DisplayRole)
        self.library_model.setHeaderData(5, Qt.Horizontal, "Date", Qt.DisplayRole)

        self.playlist_view.setModel(self.library_model)
        self.playlist_view.setEditTriggers(QAbstractItemView.NoEditTriggers)  # Disable editing
        self.playlist_view.setSortingEnabled(True)
        self.playlist_view.hideColumn(0)  # id
        self.playlist_view.hideColumn(6)  # crc32
        self.playlist_view.hideColumn(7)  # path

        self.library_model.select()  # Force-update the view

        self.play_button.pressed.connect(self.player.play)
        self.previous_button.pressed.connect(self.playlist.previous)
        self.next_button.pressed.connect(self.playlist.next)

        self.add_files_action.triggered.connect(self.add_media)

    def add_media(self):
        """Add media files selected from a file dialogue to the playlist."""
        paths, _ = QFileDialog.getOpenFileNames(self, "Add files", "", "")

        for path in paths:
            log.debug(path)
            media = QMediaContent(QUrl.fromLocalFile(path))
            library.add_media(media_utils.parse_media(path))
            self.playlist.addMedia(media)

        self.library_model.layoutChanged.emit()

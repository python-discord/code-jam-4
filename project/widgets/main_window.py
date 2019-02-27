import logging
from typing import Any, Dict

from PySide2.QtCore import Qt
from PySide2.QtMultimedia import QMediaPlayer
from PySide2.QtSql import QSqlRecord, QSqlTableModel
from PySide2.QtWidgets import QAbstractItemView, QFileDialog, QMainWindow

from project import media as media_utils
from project.playlist import Playlist
from project.ui.main_window import Ui_MainWindow

log = logging.getLogger(__name__)


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        # Model
        self.playlist_model = QSqlTableModel()
        self.playlist_model.setTable("playlist")
        self.playlist_model.setHeaderData(1, Qt.Horizontal, "Title", Qt.DisplayRole)
        self.playlist_model.setHeaderData(2, Qt.Horizontal, "Artist", Qt.DisplayRole)
        self.playlist_model.setHeaderData(3, Qt.Horizontal, "Album", Qt.DisplayRole)
        self.playlist_model.setHeaderData(4, Qt.Horizontal, "Genre", Qt.DisplayRole)
        self.playlist_model.setHeaderData(5, Qt.Horizontal, "Date", Qt.DisplayRole)

        # View
        self.playlist_view.setModel(self.playlist_model)
        self.playlist_view.setEditTriggers(QAbstractItemView.NoEditTriggers)  # Disable editing
        self.playlist_view.setSortingEnabled(True)
        self.playlist_view.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.playlist_view.setSelectionMode(QAbstractItemView.SingleSelection)
        self.playlist_view.hideColumn(0)  # id
        self.playlist_view.hideColumn(6)  # crc32
        self.playlist_view.hideColumn(7)  # path

        self.playlist_model.select()  # Force-update the view

        # Playlist
        self.player = QMediaPlayer()
        self.playlist = Playlist(self.playlist_view)
        self.playlist.setPlaybackMode(Playlist.Loop)

        # Widget signals
        self.play_button.pressed.connect(self.player.play)
        self.previous_button.pressed.connect(self.playlist.previous)
        self.next_button.pressed.connect(self.playlist.next)
        self.add_files_action.triggered.connect(self.add_media)

    def create_record(self, metadata: Dict[str, Any]) -> QSqlRecord:
        """Create and return a library record from media `metadata`.

        Parameters
        ----------
        metadata: Dict[str, Any]
            The media's metadata

        Returns
        -------
        QSqlRecord
            The created record.

        """
        record = self.playlist_model.record()
        record.remove(record.indexOf("id"))  # id field is auto-incremented so it can be removed.

        for k, v in metadata.items():
            record.setValue(k, v)

        return record

    def add_media(self):
        """Add media files selected from a file dialogue to the playlist."""
        paths, _ = QFileDialog.getOpenFileNames(self, "Add files", "", "")

        for path in paths:
            log.debug(path)

            metadata = media_utils.parse_media(path)
            record = self.create_record(metadata)

            if not self.playlist_model.insertRecord(-1, record):  # -1 will append
                log.error(f"Failed to insert record for {path}: {self.playlist_model.lastError()}")
                # TODO: Does a rollback need to happen in case of failure?

        self.playlist_model.submitAll()

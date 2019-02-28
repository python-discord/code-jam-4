import logging
from typing import Any, Dict

from PySide2.QtCore import QUrl, Qt
from PySide2.QtMultimedia import QMediaContent, QMediaPlayer
from PySide2.QtSql import QSqlRecord, QSqlTableModel
from PySide2.QtWidgets import QAbstractItemView, QFileDialog, QMainWindow

from project import media as media_utils, ui
from project.playlist import Playlist
from project.widgets.password_prompt import PasswordPrompt

log = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.ui = ui.MainWindow()
        self.ui.setupUi(self)

        self.password_prompt = PasswordPrompt()

        # Model
        self.playlist_model = QSqlTableModel()
        self.playlist_model.setTable("playlist")
        self.playlist_model.setHeaderData(1, Qt.Horizontal, "Title", Qt.DisplayRole)
        self.playlist_model.setHeaderData(2, Qt.Horizontal, "Artist", Qt.DisplayRole)
        self.playlist_model.setHeaderData(3, Qt.Horizontal, "Album", Qt.DisplayRole)
        self.playlist_model.setHeaderData(4, Qt.Horizontal, "Genre", Qt.DisplayRole)
        self.playlist_model.setHeaderData(5, Qt.Horizontal, "Date", Qt.DisplayRole)

        # View
        self.ui.playlist_view.setModel(self.playlist_model)
        self.ui.playlist_view.setEditTriggers(QAbstractItemView.NoEditTriggers)  # Disable editing
        self.ui.playlist_view.setSortingEnabled(True)
        self.ui.playlist_view.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.playlist_view.setSelectionMode(QAbstractItemView.SingleSelection)
        self.ui.playlist_view.hideColumn(0)  # id
        self.ui.playlist_view.hideColumn(6)  # crc32
        self.ui.playlist_view.hideColumn(7)  # path

        self.playlist_model.select()  # Force-update the view

        # Playlist
        self.playlist = Playlist(self.playlist_model)
        self.playlist.setPlaybackMode(Playlist.Loop)
        self.playlist.currentIndexChanged.connect(self.playlist_index_changed)

        # Player
        self.player = QMediaPlayer()
        self.player.error.connect(self.player_error)
        self.player.mediaStatusChanged.connect(self.player_media_status_changed)
        self.player.stateChanged.connect(self.player_state_changed)
        self.player.setPlaylist(self.playlist)

        # Widget signals
        self.ui.play_button.pressed.connect(self.player.play)
        self.ui.previous_button.pressed.connect(self.playlist.previous)
        self.ui.next_button.pressed.connect(self.playlist.next)
        self.ui.add_files_action.triggered.connect(self.add_media)

    def create_record(self, metadata: Dict[str, Any]) -> QSqlRecord:
        """Create and return a library record from media `metadata`.

        Parameters
        ----------
        metadata: Dict[str, Any]
            The media's metadata.

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
            log.debug(f"Adding record for {path}")

            metadata = media_utils.parse_media(path)
            record = self.create_record(metadata)

            if not self.playlist_model.insertRecord(-1, record):  # -1 will append
                log.error(f"Failed to insert record for {path}: {self.playlist_model.lastError()}")
                # TODO: Does a rollback need to happen in case of failure?
                continue

            media = QMediaContent(QUrl.fromLocalFile(path))
            if not self.playlist.addMedia(media, self.playlist_model.rowCount() - 1):
                log.error(f"Failed to add media to playlist for {path}")
                # TODO: revertAll/rollback

        self.playlist_model.submitAll()

    @staticmethod
    def player_state_changed(state):
        log.debug(f"State changed: {state}")

    @staticmethod
    def player_media_status_changed(status):
        log.debug(f"Status changed: {status}")

    def playlist_index_changed(self, index: int):
        name = self.playlist.currentMedia().canonicalUrl().fileName()
        log.debug(f"Index changed: [{index:03d}] {name}")

    def player_error(self, error):
        log.error(f"{error}: {self.player.errorString()}")

import logging

from PySide2.QtCore import Qt
from PySide2.QtSql import QSqlTableModel
from PySide2.QtWidgets import QAbstractItemView, QFileDialog, QMainWindow

from project import media, ui
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

        # Default is a descending sort, which leads to an inconsistency given media is appended
        self.playlist_model.setSort(0, Qt.AscendingOrder)
        self.playlist_model.select()  # Force-update the view

        self.player = media.Player(self.playlist_model)

        # Widget signals
        self.ui.play_button.pressed.connect(self.player.play)
        self.ui.previous_button.pressed.connect(self.player.playlist().previous)
        self.ui.next_button.pressed.connect(self.player.playlist().next)
        self.ui.add_files_action.triggered.connect(self.add_files)

    def add_files(self, checked: bool = False):
        """Show a file dialogue and add selected files to the playlist."""
        paths, _ = QFileDialog.getOpenFileNames(self, "Add files", "", "")
        self.player.add_media(paths)

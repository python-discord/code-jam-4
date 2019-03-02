import logging

from PySide2.QtCore import QPoint, Qt
from PySide2.QtSql import QSqlTableModel
from PySide2.QtWidgets import (
    QAbstractItemView, QAction, QFileDialog, QMainWindow, QMenu
)

from project import media, ui
from project.widgets.password_prompt import PasswordPrompt
from project.widgets.create_password import CreatePassword

log = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.ui = ui.MainWindow()
        self.ui.setupUi(self)

        self.password_prompt = PasswordPrompt('temporarypassword')

        self.playlist_model = self.create_model()
        self.configure_view()

        self.player = media.Player(self.playlist_model)

        # Signal connections
        self.ui.play_button.pressed.connect(self.player.play)
        self.ui.previous_button.pressed.connect(self.player.playlist().previous)
        self.ui.next_button.pressed.connect(self.player.playlist().next)
        self.ui.add_files_action.triggered.connect(self.add_files)

    @staticmethod
    def create_model() -> QSqlTableModel:
        """Create and return the model to use with the playlist table view."""
        model = QSqlTableModel()
        model.setTable("playlist")
        model.setEditStrategy(QSqlTableModel.OnManualSubmit)

        model.setHeaderData(1, Qt.Horizontal, "Title", Qt.DisplayRole)
        model.setHeaderData(2, Qt.Horizontal, "Artist", Qt.DisplayRole)
        model.setHeaderData(3, Qt.Horizontal, "Album", Qt.DisplayRole)
        model.setHeaderData(4, Qt.Horizontal, "Genre", Qt.DisplayRole)
        model.setHeaderData(5, Qt.Horizontal, "Date", Qt.DisplayRole)

        # Default is a descending sort, which leads to an inconsistency given media is appended
        model.setSort(0, Qt.AscendingOrder)
        model.select()  # Force-update the view

        return model

    def configure_view(self):
        """Configure the playlist table view."""
        self.ui.playlist_view.setModel(self.playlist_model)
        self.ui.playlist_view.setEditTriggers(QAbstractItemView.NoEditTriggers)  # Disable editing
        self.ui.playlist_view.setSortingEnabled(True)

        self.ui.playlist_view.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.playlist_view.setSelectionMode(QAbstractItemView.SingleSelection)

        self.ui.playlist_view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.playlist_view.customContextMenuRequested.connect(self.show_view_context_menu)

        self.ui.playlist_view.hideColumn(0)  # id
        self.ui.playlist_view.hideColumn(6)  # crc32
        self.ui.playlist_view.hideColumn(7)  # path

    def create_view_context_menu(self, pos: QPoint) -> QMenu:
        """Create and return a context menu to use with the playlist view."""
        menu = QMenu()
        remove_action = QAction("Remove", self.ui.playlist_view)
        menu.addAction(remove_action)

        row = self.ui.playlist_view.rowAt(pos.y())
        remove_action.triggered.connect(lambda: self.player.remove_media(row))

        return menu

    def show_view_context_menu(self, pos: QPoint):
        """Display a context menu for the table view."""
        menu = self.create_view_context_menu(pos)
        self.ui.playlist_view.context_menu = menu  # Prevents it from being GC'd

        global_pos = self.ui.playlist_view.mapToGlobal(pos)
        menu.popup(global_pos)

    def add_files(self, checked: bool = False):
        """Show a file dialogue and add selected files to the playlist."""
        paths, _ = QFileDialog.getOpenFileNames(self, "Add files", "", "")
        self.player.add_media(paths)

import logging
import random

from PySide2.QtCore import QPoint, Qt
from PySide2.QtGui import QMouseEvent
from PySide2.QtSql import QSqlTableModel
from PySide2.QtWidgets import (
    QAction, QDialog, QFileDialog, QHeaderView, QMainWindow, QMenu, QMessageBox
)

from project import media, ui
from project.delegates import CurrentMediaDelegate
from project.widgets.captcha_dialogue import CaptchaDialogue
from project.widgets.password_prompt import PasswordPrompt
from project.widgets.seek_dialogue import SeekDialogue

log = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    def __init__(self, password, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.ui = ui.MainWindow()
        self.ui.setupUi(self)

        self.password_prompt = PasswordPrompt(password)

        self.captcha_dialogue = CaptchaDialogue(self)
        self.captcha_dialogue.finished.connect(self.add_files)

        self.seek_dialogue = SeekDialogue(self)
        self.seek_dialogue.finished.connect(self.seek_finished)

        self.playlist_model = self.create_model()
        self.configure_view()
        self.current_delegate = CurrentMediaDelegate()

        self.player = media.Player(self.playlist_model)
        self.player.durationChanged.connect(self.ui.seek_slider.setMaximum)
        self.player.durationChanged.connect(self.seek_dialogue.update_duration)
        self.player.positionChanged.connect(self.ui.seek_slider.setValue)
        self.player.positionChanged.connect(self.update_time_remaining)
        self.player.stateChanged.connect(self.toggle_button_text)

        # Style the current row
        header = self.ui.playlist_view.horizontalHeader()
        header.sortIndicatorChanged.connect(self.style_current_row)
        self.player.currentMediaChanged.connect(self.style_current_row)
        self.player.media_added.connect(self.style_current_row)
        self.player.media_removed.connect(self.style_current_row)

        self.ui.seek_slider.mousePressEvent = self.seek_slider_pressed  # Override the event

        # Signal connections
        self.ui.play_button.pressed.connect(self.play_pressed)
        self.ui.previous_button.pressed.connect(self.player.playlist().previous)
        self.ui.next_button.pressed.connect(self.player.playlist().next)
        self.ui.add_files_action.triggered.connect(self.captcha_dialogue.open)

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
        self.ui.playlist_view.customContextMenuRequested.connect(self.show_view_context_menu)
        self.ui.playlist_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.playlist_view.hideColumn(0)  # id
        self.ui.playlist_view.hideColumn(6)  # crc32
        self.ui.playlist_view.hideColumn(7)  # path

    def create_view_context_menu(self, pos: QPoint) -> QMenu:
        """Create and return a context menu to use with the playlist view."""
        menu = QMenu()
        remove_action = QAction("Remove", self.ui.playlist_view)
        menu.addAction(remove_action)

        row = self.ui.playlist_view.rowAt(pos.y())
        remove_action.triggered.connect(lambda: self.remove_triggered(row))

        return menu

    def show_view_context_menu(self, pos: QPoint):
        """Display a context menu for the table view."""
        menu = self.create_view_context_menu(pos)
        self.ui.playlist_view.context_menu = menu  # Prevents it from being GC'd

        global_pos = self.ui.playlist_view.mapToGlobal(pos)
        menu.popup(global_pos)

    def remove_triggered(self, row: int):
        """Show confirmation message boxes and remove the media at `row`."""
        title = self.playlist_model.index(row, 1).data()

        result_1 = QMessageBox.question(
            self,
            "Remove Media",
            f"Are you sure you want to remove {title}?"
        )

        if result_1 != QMessageBox.Yes:
            return

        result_2 = QMessageBox.question(
            self,
            "Remove Media",
            f"Are you <i>really</i> sure?",
            QMessageBox.Yes | QMessageBox.No
        )

        if result_2 != QMessageBox.Yes:
            return

        result_3 = QMessageBox.warning(
            self,
            "Remove Media",
            f"Are you <i>really really</i> sure?",
            QMessageBox.Yes | QMessageBox.No
        )

        if result_3 == QMessageBox.Yes:
            self.player.remove_media(row)

    def update_time_remaining(self, position: int):
        """Update the time remaining for the current track on the LCD."""
        remaining = self.player.duration() - position
        self.ui.media_time_lcd.display(remaining // 1000)

    def seek_slider_pressed(self, event: QMouseEvent):
        """Open the seek dialogue when the slider is left clicked."""
        if self.player.playlist().currentMedia().isNull():
            return

        if event.button() == Qt.LeftButton:
            pos = self.player.position()
            self.seek_dialogue.update_position(pos)
            self.seek_dialogue.open()

    def seek_finished(self, result: QDialog.DialogCode):
        """Seek to the selected position if the seek dialogue was accepted."""
        if result == QDialog.DialogCode.Accepted:
            pos = self.seek_dialogue.get_position()
            self.player.setPosition(pos)

    def play_pressed(self):
        """Play or pause the player depending on its state."""
        if random.randint(0, 3) == 0:
            self.password_prompt.display()
            if self.password_prompt.success:
                pass
            else:
                return
        self.password_prompt.display()
        if self.player.state() in (media.Player.StoppedState, media.Player.PausedState):
            self.player.play()
        else:
            self.player.pause()

    def toggle_button_text(self, state: media.Player.State):
        """Set the text of the play button depending on the player's state."""
        if state in (media.Player.StoppedState, media.Player.PausedState):
            self.ui.play_button.setText("Play")
        else:
            self.ui.play_button.setText("Pause")

    def style_current_row(self, *args):
        """Set a custom delegate for the row corresponding to the current media."""
        current_row = self.player.playlist().currentIndex()

        # Clear custom delegate from any other rows
        for row in range(self.playlist_model.rowCount()):
            self.ui.playlist_view.setItemDelegateForRow(row, None)

        if current_row == -1:
            return

        # TODO: Clear delegate for previous row
        self.ui.playlist_view.setItemDelegateForRow(current_row, self.current_delegate)

    def add_files(self, result: QDialog.DialogCode):
        """Show a file dialogue and add selected files to the playlist."""
        if result == QDialog.DialogCode.Accepted:
            paths, _ = QFileDialog.getOpenFileNames(self, "Add files", "", "")
            self.player.add_media(paths)

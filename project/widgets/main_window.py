from PySide2.QtCore import QUrl
from PySide2.QtMultimedia import QMediaContent, QMediaPlayer, QMediaPlaylist
from PySide2.QtWidgets import QFileDialog, QMainWindow

from project.models.playlist import PlaylistModel
from project.ui.main_window import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.player = QMediaPlayer()
        self.playlist = QMediaPlaylist()

        self.playlist_model = PlaylistModel(self.playlist)
        self.playlist_view.setModel(self.playlist_model)

        self.play_button.pressed.connect(self.player.play)
        self.previous_button.pressed.connect(self.playlist.previous)
        self.next_button.pressed.connect(self.playlist.next)

        self.add_files_action.triggered.connect(self.add_media)

    def add_media(self):
        """Add media files selected from a file dialogue to the playlist."""
        paths, _ = QFileDialog.getOpenFileNames(self, "Add files", "", "")

        for path in paths:
            print(path)
            media = QMediaContent(QUrl.fromLocalFile(path))
            self.playlist.addMedia(media)

        self.playlist_model.layoutChanged.emit()

from PySide2.QtCore import QAbstractTableModel, Qt


class PlaylistModel(QAbstractTableModel):
    def __init__(self, playlist, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.playlist = playlist

    def data(self, index, role=None):
        if role != Qt.DisplayRole:
            return

        media = self.playlist.media(index.row())

        # TODO: Get metadata via ffprobe
        return media.canonicalUrl().fileName()

    def headerData(self, section, orientation, role=None):
        if role != Qt.DisplayRole:
            return

        if orientation == Qt.Horizontal:
            if section == 0:
                return "Filename"

    def columnCount(self, parent=None, *args, **kwargs):
        return 1

    def rowCount(self, parent=None, *args, **kwargs):
        return self.playlist.mediaCount()

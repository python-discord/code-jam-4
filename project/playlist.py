import logging
import sqlite3

from PySide2.QtCore import QModelIndex, QUrl
from PySide2.QtMultimedia import QMediaContent, QMediaPlaylist
from PySide2.QtSql import QSqlDatabase
from PySide2.QtWidgets import QAbstractItemView

log = logging.getLogger(__name__)

DB_NAME = "library.sqlite"


class Playlist(QMediaPlaylist):
    def __init__(self, view: QAbstractItemView, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.view = view
        self._model = view.model()

        self._current_index: QModelIndex = None
        self._current_media: QMediaContent = None
        self.setCurrentIndex(0)

    def currentIndex(self):
        if self._current_index is not None:
            return self._current_index.row()

    def currentMedia(self):
        return self._current_media

    def isEmpty(self):
        return self.mediaCount() == 0

    def isReadOnly(self):
        return True

    def media(self, index: int):
        # TODO: This shortcut may backfire if this method is intended to update media when sort
        # changes but the current index does not.
        if index == self.currentIndex():
            return self._current_media

        record = self._model.record(index)
        path = record.field("path").value()
        return QMediaContent(QUrl.fromLocalFile(path))

    def mediaCount(self):
        return self._model.rowCount()

    def nextIndex(self, steps: int = 1):
        mode = self.playbackMode()
        index = self.currentIndex()
        total = self.mediaCount()

        if index is None:
            return None  # TODO: Properly handle this

        if index + steps >= total:
            if mode == self.Sequential:
                return None
            elif mode == self.Loop:
                return (index + steps) % total
            else:
                raise NotImplementedError  # TODO: Support other modes
        else:
            return index + steps

    def previousIndex(self, steps: int = 1):
        mode = self.playbackMode()
        index = self.currentIndex()
        total = self.mediaCount()

        if index is None:
            return None  # TODO: Properly handle this

        if index - steps < 0:
            if mode == self.Sequential:
                return None
            elif mode == self.Loop:
                return total + (index - steps)
            else:
                raise NotImplementedError  # TODO: Support other modes
        else:
            return index - steps

    def next(self):
        self.setCurrentIndex(self.nextIndex())
        log.debug(f"next: {self.currentIndex()}")

    def previous(self):
        self.setCurrentIndex(self.previousIndex())
        log.debug(f"previous: {self.currentIndex()}")

    def setCurrentIndex(self, index: int):
        if index is None:
            self._current_index = None
            self._current_media = None
        else:
            self._current_index = self._model.index(index, 0)
            self._current_media = self.media(self.currentIndex())

    def shuffle(self):
        raise NotImplementedError  # TODO: Implement

    def addMedia(self, *args, **kwargs):
        raise NotImplementedError

    def clear(self, *args, **kwargs):
        raise NotImplementedError

    def insertMedia(self, *args, **kwargs):
        raise NotImplementedError

    def load(self, *args, **kwargs):
        raise NotImplementedError

    def moveMedia(self, *args, **kwargs):
        raise NotImplementedError

    def removeMedia(self, *args, **kwargs):
        raise NotImplementedError

    def save(self, *args, **kwargs):
        raise NotImplementedError


def create_db():
    """Create the playlist's database file and table if they don't exist.

    The created database should be accessed using :meth:`PySide2.QtSql.QSqlDatabase.database`, the
    name being specified via :const:`project.library.DB_NAME`.

    """
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            create table if not exists playlist (
                id     integer primary key,
                title  text,
                artist text,
                album  text,
                genre  text,
                date   text,
                crc32  integer not null,
                path   text    not null
            );
        """)
        conn.commit()

    db = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName(DB_NAME)

    # TODO: Handle possible errors if db fails to open

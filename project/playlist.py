import logging
import sqlite3
from pathlib import Path

from bidict import bidict
from PySide2.QtCore import QAbstractItemModel, QUrl, Qt
from PySide2.QtMultimedia import QMediaContent, QMediaPlaylist
from PySide2.QtSql import QSqlDatabase

log = logging.getLogger(__name__)

DB_NAME = "library.sqlite"


class Playlist(QMediaPlaylist):
    """A wrapper for :class:`QMediaPlaylist` which navigates using a :class:`QAbstractItemModel`.

    Rather than using the :class:`QMediaPlaylist`'s regular internal data structure for determining
    the previous or next media, a :class:`QAbstractItemModel` is used. This means that
    :meth:`Playlist.next()` and :meth:`Playlist.previous()` will account for the order of the items
    in the model changing.

    This works on the basic principle of using a dictionary to map media ids (the primary keys) to
    indices in the playlist's internal data structure.

    The playback mode :attr:`QMediaPlaylist.Random` is currently unsupported.

    """
    def __init__(self, model: QAbstractItemModel, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._model = model
        self._indices = bidict()  # media_id: playlist_index
        self._current_media = QMediaContent()
        self._current_index = -1

        self._populate()

    def _get_playlist_index(self, row: int) -> int:
        """Return the playlist index which corresponds to the `row`."""
        if row == -1:
            return -1

        media_id = self._model.index(row, 0).data()
        return self._indices[media_id]

    def _get_row(self, playlist_index: int) -> int:
        """Return the row index which corresponds to the `playlist_index`."""
        if playlist_index == -1:
            return -1

        # The data of each item in the model just contains the value of the table's "id" field.
        # This searches the data of each item in the model for the media_id. Once the index
        # is obtained from the search results, the row index can easily be retrieved.
        media_id = self._indices.inverse[playlist_index]
        start_index = self._model.index(0, 0)
        matches = self._model.match(start_index, Qt.DisplayRole, media_id, flags=Qt.MatchExactly)

        return matches[0].row()  # ids are unique so there should always only be one match anyway.

    def _jump(self, index: int):
        """Set the current index and media to `index`."""
        log.debug(f"Jumping to index {index}")
        if index < -1 or index >= self.mediaCount():
            index = -1

        if index != -1:
            self._current_media = self.media(index)
        else:
            self._current_media = QMediaContent()

        if index != self.currentIndex():
            self._current_index = index
            self.currentIndexChanged.emit(self._current_index)
            # self.surroundingItemsChanged.emit()

        # This should be equivalent to QMediaPlaylistNavigator's "activate" signal
        self.currentMediaChanged.emit(self._current_media)

    def _populate(self):
        """Populate the playlist with existing media in the model."""
        for row in range(self._model.rowCount()):
            path = self._model.index(row, 7).data()
            if Path(path).is_file():
                media = QMediaContent(QUrl.fromLocalFile(path))
                if not self.addMedia(media, row):
                    # TODO: Prompt user to remove from model on failure
                    log.warning(
                        f"Could not populate playlist for row {row}: "
                        f"adding media for {path} failed."
                    )
            else:
                # TODO: Prompt user to remove from model on failure
                log.warning(
                    f"Could not populate playlist for row {row}: "
                    f"{path} does not exist or isn't a file."
                )

    def currentIndex(self) -> int:
        return self._current_index

    def setCurrentIndex(self, index: int):
        log.debug(f"Setting index to {index}")
        self._jump(index)

    def currentMedia(self) -> QMediaContent:
        return self._current_media

    def addMedia(self, content: QMediaContent, row: int) -> bool:
        log.debug(f"Adding media for row {row}: {content.canonicalUrl().fileName()}")
        success = super().addMedia(content)

        if success:
            media_id = self._model.index(row, 0).data()
            self._indices[media_id] = self.mediaCount() - 1
            log.debug(
                f"Successfully added media: media id {media_id}; "
                f"playlist index {self._indices[media_id]}"
            )

        return success

    def moveMedia(self, *args, **kwargs):
        raise NotImplementedError

    def removeMedia(self, index: int):
        log.debug(f"Adding media for index {index}.")
        success = super().removeMedia(index)

        if success:
            row = self._get_row(index)

            # TODO: Handle partial removals better. Maybe re-add media to playlist?
            if not self._model.removeRow(row):
                log.error(
                    f"Media was only partially removed: "
                    f"failed to remove media at row {row} from model."
                )
                return False

        return success

    def nextIndex(self, steps: int = 1) -> int:
        if self.mediaCount() == 0:
            return -1

        if steps == 0:
            return self.currentIndex()

        next_row = -1
        current_row = self._get_row(self.currentIndex())
        mode = self.playbackMode()

        if mode == self.CurrentItemOnce:
            return -1
        elif mode == self.CurrentItemInLoop:
            return self.currentIndex()
        elif mode == self.Sequential:
            next_pos = current_row + steps
            next_row = next_pos if next_pos < self.mediaCount() else -1
        elif mode == self.Loop:
            next_row = (current_row + steps) % self.mediaCount()
        elif mode == self.Random:
            raise NotImplementedError  # TODO: Support Random mode

        return self._get_playlist_index(next_row)

    def previousIndex(self, steps: int = 1) -> int:
        if self.mediaCount() == 0:
            return -1

        if steps == 0:
            return self.currentIndex()

        prev_row = -1
        current_row = self._get_row(self.currentIndex())
        mode = self.playbackMode()

        if mode == self.CurrentItemOnce:
            return -1
        elif mode == self.CurrentItemInLoop:
            return self.currentIndex()
        elif mode == self.Sequential:
            prev_pos = self.mediaCount() - steps if current_row == -1 else current_row - 1
            prev_row = prev_pos if prev_pos >= 0 else -1
        elif mode == self.Loop:
            prev_pos = current_row - steps

            while prev_pos < 0:
                prev_pos += self.mediaCount()

            prev_row = prev_pos
        elif mode == self.Random:
            raise NotImplementedError  # TODO: Support Random mode

        return self._get_playlist_index(prev_row)

    def next(self):
        self._jump(self.nextIndex())

    def previous(self):
        self._jump(self.previousIndex())

    def clear(self):
        raise NotImplementedError

    def shuffle(self):
        raise NotImplementedError

    def load(self, *args, **kwargs):
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

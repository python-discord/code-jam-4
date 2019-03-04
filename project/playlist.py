import logging
from pathlib import Path
from typing import Dict

from PySide2.QtCore import QAbstractItemModel, QUrl, Qt
from PySide2.QtMultimedia import QMediaContent, QMediaPlaylist

log = logging.getLogger(__name__)


class Playlist(QMediaPlaylist):
    """A wrapper for :class:`QMediaPlaylist` which navigates using a :class:`QAbstractItemModel`.

    Rather than using the :class:`QMediaPlaylist`'s regular internal data structure for determining
    the previous or next media, the rows of a :class:`QAbstractItemModel` are used. This means that
    :meth:`Playlist.next()` and :meth:`Playlist.previous()` will account for the order of the rows
    in the model changing.

    This works by fetching the media id (the primary key) from the model for a given row.

    The playback mode :attr:`QMediaPlaylist.Random` is currently unsupported.

    """
    def __init__(self, model: QAbstractItemModel, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._model = model
        self._media: Dict[int, QMediaContent] = {}
        self._current_media = -1

        self._populate()

    def _get_media_id(self, row: int) -> int:
        """Return the media ID corresponding to the `row`."""
        return self._model.index(row, 0).data()

    def _get_row(self, media_id: int) -> int:
        """Return the row index which corresponds to the `media_id`."""
        if media_id == -1:
            return -1

        start_index = self._model.index(0, 0)
        matches = self._model.match(start_index, Qt.DisplayRole, media_id, flags=Qt.MatchExactly)

        return matches[0].row()  # ids are unique so there should always only be one match anyway.

    def _jump(self, index: int):
        """Set the current index and media to `index`."""
        log.debug(f"Jumping to index {index}")
        if index < -1 or index >= self.mediaCount():
            index = -1

        if index != -1:
            self._current_media = self._get_media_id(index)
        else:
            self._current_media = -1

        if index != self.currentIndex():
            self.currentIndexChanged.emit(index)
            # self.surroundingItemsChanged.emit()

        # This should be equivalent to QMediaPlaylistNavigator's "activate" signal
        self.currentMediaChanged.emit(self.currentMedia())

    def _populate(self):
        """Populate the playlist with existing media in the model."""
        for row in range(self._model.rowCount()):
            path = self._model.index(row, 7).data()
            if Path(path).is_file():
                media = QMediaContent(QUrl.fromLocalFile(path))
                media_id = self._get_media_id(row)
                self.addMedia(media, media_id)
            else:
                # TODO: Prompt user to remove from model on failure
                log.warning(
                    f"Could not populate playlist for row {row}: "
                    f"{path} does not exist or isn't a file."
                )

    def currentIndex(self) -> int:
        return self._get_row(self._current_media)

    def setCurrentIndex(self, index: int):
        log.debug(f"Setting index to {index}")
        self._jump(index)

    def currentMedia(self) -> QMediaContent:
        if self._current_media == -1:
            return QMediaContent()

        return self._media[self._current_media]

    def addMedia(self, content: QMediaContent, media_id: int) -> bool:
        """Append the media `content` to the playlist.

        Parameters
        ----------
        content: QMediaContent
            The media to append.
        media_id: int
            The ID of the media in the model.

        Returns
        -------
        bool
            Always True.

        """
        row = self._get_row(media_id)

        self.mediaAboutToBeInserted.emit(row, row)
        self._media[media_id] = content
        self.mediaInserted.emit(row, row)

        file_name = content.canonicalUrl().fileName()
        log.debug(f"Added media with ID {media_id}: {file_name}")

        return True

    def insertMedia(self, *args, **kwargs):
        raise NotImplementedError

    def moveMedia(self, *args, **kwargs):
        raise NotImplementedError

    def removeMedia(self, index: int) -> bool:
        """Remove the media at row `index` from the playlist.

        Parameters
        ----------
        index: int
            The row in the model which corresponds to the media.

        Returns
        -------
        bool
            Always True.

        """
        media_id = self._get_media_id(index)

        self.mediaAboutToBeRemoved.emit(index, index)
        del self._media[media_id]
        self.mediaRemoved.emit(index, index)

        log.debug(f"Removed media at row {index}, media_id {media_id}.")

        if index == self.currentIndex():
            # Effectively stops the playlist if the current media is removed.
            self.setCurrentIndex(-1)

        return True

    def nextIndex(self, steps: int = 1) -> int:
        if self.mediaCount() == 0:
            return -1

        if steps == 0:
            return self.currentIndex()

        mode = self.playbackMode()

        if mode == self.CurrentItemOnce:
            return -1
        elif mode == self.CurrentItemInLoop:
            return self.currentIndex()
        elif mode == self.Sequential:
            next_pos = self.currentIndex() + steps
            return next_pos if next_pos < self.mediaCount() else -1
        elif mode == self.Loop:
            return (self.currentIndex() + steps) % self.mediaCount()
        elif mode == self.Random:
            raise NotImplementedError  # TODO: Support Random mode

    def previousIndex(self, steps: int = 1) -> int:
        if self.mediaCount() == 0:
            return -1

        if steps == 0:
            return self.currentIndex()

        mode = self.playbackMode()

        if mode == self.CurrentItemOnce:
            return -1
        elif mode == self.CurrentItemInLoop:
            return self.currentIndex()
        elif mode == self.Sequential:
            if self.currentIndex() == -1:
                prev_pos = self.mediaCount() - steps
            else:
                prev_pos = self.currentIndex() - 1

            return prev_pos if prev_pos >= 0 else -1
        elif mode == self.Loop:
            prev_pos = self.currentIndex() - steps

            while prev_pos < 0:
                prev_pos += self.mediaCount()

            return prev_pos
        elif mode == self.Random:
            raise NotImplementedError  # TODO: Support Random mode

    def next(self):
        self._jump(self.nextIndex())

    def previous(self):
        self._jump(self.previousIndex())

    def media(self, index: int) -> QMediaContent:
        if index == -1:
            return QMediaContent()

        media_id = self._get_media_id(index)
        return self._media[media_id]

    def mediaCount(self) -> int:
        return len(self._media)

    def clear(self):
        raise NotImplementedError

    def shuffle(self):
        raise NotImplementedError

    def load(self, *args, **kwargs):
        raise NotImplementedError

    def save(self, *args, **kwargs):
        raise NotImplementedError

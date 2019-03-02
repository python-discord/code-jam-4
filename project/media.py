import binascii
import json
import logging
import subprocess
from pathlib import Path
from typing import Any, Dict, Iterable

from PySide2.QtCore import QUrl
from PySide2.QtMultimedia import QMediaContent, QMediaPlayer
from PySide2.QtSql import QSqlRecord, QSqlTableModel

from project.playlist import Playlist

log = logging.getLogger(__name__)

TAG_WHITELIST = ("title", "artist", "album", "date", "genre")


def _compute_crc32(path: str) -> int:
    """Compute and return the CRC-32 of a file at `path`.

    Parameters
    ----------
    path: str
        The path to the file.

    Returns
    -------
    int
        The CRC-32 of the data in the file.

    """
    with open(path, "rb") as file:
        data = file.read()
        return binascii.crc32(data)


def _parse_media(path: str):
    """Parse the metadata of a media file and return it as a dictionary.

    Parameters
    ----------
    path: str
        The path to the media file.

    Returns
    -------
    dict
        The media's metadata.

    """
    args = [
        "ffprobe",
        "-hide_banner",
        "-loglevel", "error",
        "-of", "json",
        "-show_entries", "format_tags",
        path
    ]

    process = subprocess.run(args, capture_output=True, encoding="utf-8")
    tags = dict()

    if process.returncode != 0:
        log.error(f"Failed to fetch metadata for {path}: return code {process.returncode}")
        log.debug(process.stderr)

    try:
        metadata = json.loads(process.stdout, encoding="utf-8")
        tags = metadata["format"]["tags"]
    except (json.JSONDecodeError, KeyError):
        log.exception("Failed to parse metadata for {path}")

    # Filter out unsupported tags and make them all lowercase.
    tags = {k.lower(): v for k, v in tags.items() if k.lower() in TAG_WHITELIST}

    tags["path"] = path
    tags["crc32"] = _compute_crc32(path)

    # Use the file name as the title if one doesn't exist.
    if not tags.get("title"):
        tags["title"] = Path(path).stem

    return tags


class Player(QMediaPlayer):
    def __init__(self, model: QSqlTableModel, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._model = model

        playlist = Playlist(self._model)
        playlist.setPlaybackMode(Playlist.Loop)
        playlist.currentIndexChanged.connect(self.playlist_index_changed)

        self.error.connect(self.handle_error)
        self.mediaStatusChanged.connect(self.media_status_changed)
        self.stateChanged.connect(self.state_changed)
        self.setPlaylist(playlist)

    def _create_record(self, metadata: Dict[str, Any]) -> QSqlRecord:
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
        record = self._model.record()
        record.remove(record.indexOf("id"))  # id field is auto-incremented so it can be removed.

        for k, v in metadata.items():
            record.setValue(k, v)

        return record

    def add_media(self, paths: Iterable[str]):
        """Add media from `paths` to the playlist.

        Parameters
        ----------
        paths: Iterable[str]
            The paths to the media files to add.

        """
        # TODO: Let's just hope the commits and rollbacks always succeed for now...
        self._model.database().transaction()
        start_row = self._model.rowCount()
        paths_added = []

        for path in paths:
            log.debug(f"Adding media for {path}")

            metadata = _parse_media(path)
            record = self._create_record(metadata)

            if not self._model.insertRecord(-1, record):  # -1 will append
                log.error(f"Failed to add media for {path}: {self._model.lastError()}")
                # Assuming the model wasn't ever modified if this failed; no revert needed.
            else:
                paths_added.append(path)

        if not self._model.submitAll():
            log.error(f"Failed to add media: could not submit changes.")
            self._model.revertAll()
            self._model.database().rollback()

            return

        self._model.database().commit()

        for row, path in enumerate(paths, start_row):
            media = QMediaContent(QUrl.fromLocalFile(path))
            self.playlist().addMedia(media, row)

    def remove_media(self, row: int) -> bool:
        # TODO: Let's just hope the commits and rollbacks always succeed for now...
        self._model.database().transaction()

        if not self._model.removeRow(row):
            log.error(f"Failed to remove media at row {row} from the db: {self._model.lastError()}")
            self._model.revertAll()
            self._model.database().rollback()
            return False

        self.playlist().removeMedia(row)

        if self._model.submitAll():
            self._model.database().commit()
            return True
        else:
            log.error(f"Failed to remove media at row {row}: could not submit changes.")
            self._model.revertAll()
            self._model.database().rollback()

            # Re-add the media. It should still be in the model if it was correctly reverted.
            path = self._model.index(row, 7).data()
            media = QMediaContent(QUrl.fromLocalFile(path))
            self.playlist().addMedia(media, row)

            return False

    def play(self):
        super().play()

        if self.playlist().currentIndex() == -1:
            self.playlist().setCurrentIndex(0)

    @staticmethod
    def state_changed(state):
        log.debug(f"State changed: {state}")

    @staticmethod
    def media_status_changed(status):
        log.debug(f"Status changed: {status}")

    def playlist_index_changed(self, index: int):
        name = self.playlist().currentMedia().canonicalUrl().fileName()
        log.debug(f"Index changed: [{index:03d}] {name}")

    def handle_error(self, error):
        log.error(f"{error}: {self.player.errorString()}")

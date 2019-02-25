import binascii
import json
import logging
import subprocess

log = logging.getLogger(__name__)

TAG_WHITELIST = ("title", "artist", "album", "date", "genre")


def compute_crc32(path: str) -> int:
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


def parse_media(path: str):
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

    try:
        metadata = json.loads(process.stdout, encoding="utf-8")
        tags = metadata["format"]["tags"]
    except (json.JSONDecodeError, KeyError):
        log.exception("Failed to parse metadata for {path}")

    # Filter out unsupported tags and make them all lowercase.
    tags = {k.lower(): v for k, v in tags.items() if k.lower() in TAG_WHITELIST}

    tags["path"] = path
    tags["crc32"] = compute_crc32(path)

    return tags

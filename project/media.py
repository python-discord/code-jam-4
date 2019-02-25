import binascii
import json
import subprocess

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

    process = subprocess.run(args, capture_output=True)

    process.check_returncode()  # TODO: Handle exception better
    output = process.stdout.strip().split("\n")

    try:
        metadata = json.loads(output, encoding="utf-8")
    except json.JSONDecodeError:
        raise  # TODO: Handle exception better

    try:
        tags = metadata["format"]["tags"]
    except KeyError:
        raise  # TODO: Handle exception better

    tags = {k: v for k, v in tags.items() if k.lower() in TAG_WHITELIST}  # Filter out tags
    tags["path"] = path
    tags["crc32"] = compute_crc32(path)

    return tags

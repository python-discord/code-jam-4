from pathlib import Path

SRC: Path = Path(__file__).parent
ROOT: Path = SRC.parent
RES: Path = ROOT / 'res'

SETTINGS: Path = RES / 'settings.ini'
THEME: Path = RES / 'widgets.ini'
IMAGES: Path = RES / 'images'
SOUNDS: Path = RES / 'sounds'

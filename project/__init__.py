import logging
import os
import sys

DEBUG = os.environ.get('DEBUG', False)

logging.basicConfig(
    format='%(asctime)s | %(name)-24s | %(levelname)-8s | %(message)s',
    level=logging.DEBUG if DEBUG else logging.INFO,
    handlers=(logging.StreamHandler(stream=sys.stdout),)
)

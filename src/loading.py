from time import sleep
from PIL import Image, ImageTk
from contextlib import suppress
from itertools import cycle
from typing import Callable

from .widget import PrimaryCanvas
from . import IMAGES


def generate_frames(im: Image):
    with suppress(EOFError):
        while True:
            im.seek(im.tell()+1)
            yield ImageTk.PhotoImage(im)


class Loading(PrimaryCanvas):
    image = IMAGES / "loading.gif"
    limit = 1 / 20
    active = True

    def init(self):
        self.frames = generate_frames(Image.open(self.image))

    def waitfor(self, condition: Callable, cmd: Callable = None, args=()):
        for im in cycle(self.frames):
            if not self.active:
                break
            if condition():
                if cmd is not None:
                    cmd(*args)
                break
            self.last = self.create_image(-40.5, 0, image=im, anchor='nw')
            self.update_idletasks()
            sleep(self.limit)

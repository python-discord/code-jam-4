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
    last = 0
    limit = 1 / 20

    def init(self):
        self.frames = generate_frames(Image.open(self.image))

    def waitfor(self, condition: Callable, cmd: Callable = None, args=()):
        for im in cycle(self.frames):
            if condition():
                if cmd is not None:
                    cmd(*args)
                break
            if self.last:
                self.delete(self.last)
            self.last = self.create_image(0, 0, image=im, anchor='nw')
            self.update()
            sleep(self.limit)

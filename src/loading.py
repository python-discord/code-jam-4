from PIL import Image, ImageTk
from time import sleep
from contextlib import suppress
from itertools import cycle

from .widget import SecondaryCanvas
from . import IMAGES

def generate_frames(im: Image):
    with suppress(EOFError):
        while True:
            im.seek(im.tell()+1)
            yield ImageTk.PhotoImage(im)

class Loading(SecondaryCanvas):
    frames = generate_frames(Image.open(IMAGES / "loading.gif"))
    active = True
    last = 0

    def start(self):
        for im in cycle(self.frames):
            if not self.active:
                break
            if self.last:
                self.delete(self.last)
            self.last = self.create_image(0, 0, image=im, anchor='nw')
            self.update()

    def stop(self):
        self.active = False
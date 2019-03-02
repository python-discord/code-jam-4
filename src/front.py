import io
from PIL import Image, ImageTk

from . import widget
from .animate import Direction
from .view import Window, View
from .cache import ImageCache


def process_image(image: bytes, width: int, height: int):
    im = Image.open(io.BytesIO(image))
    im = im.resize((width, height), Image.NEAREST)
    return ImageTk.PhotoImage(im)


class Front(widget.PrimaryFrame):

    cachesize = 20

    # Quick fix to keep a reference count on the
    # last image, making sure the garbage collector
    # doesn't delete it before the animation ends
    _last = None

    def __next(self, direction: Direction = None):
        data: dict = self.cache.next()
        image = process_image(
            data.pop('image'),
            self.window.winfo_width(),
            self.window.winfo_height()
        )
        name = data.pop('name')
        self.__load(name, image, data)
        if direction is None:
            self.window.set_view(self.image)
        else:
            self.window.change_view(self.image, direction)

    def __load(self, name, image, data):
        self.title.config(text=name)
        self.image = View(image, 'image')
        self.bio = View(Bio(self.window), 'widget')

        self._last = self.image
        self.bio.data.load(data)
        self.update()

    def init(self):
        self.title = widget.PrimaryLabel(self)
        self.window = Window(self)
        self.commandbar = widget.SecondaryFrame(self)

        self.bio = None
        self.image = None

        self.btn_dislike = widget.PrimaryButton(
            self.commandbar, text='Nope', bg='red', command=self.cmd_dislike
        )
        self.btn_bio = widget.PrimaryButton(
            self.commandbar, text='Bio', command=self.cmd_bio
        )
        self.btn_like = widget.PrimaryButton(
            self.commandbar, text='Yep', bg='green', command=self.cmd_like
        )
        self.title.pack(fill='x', expand=True)
        self.window.pack(fill='both', expand=True)
        self.commandbar.pack(side='bottom', fill='x', expand=True)

        self.btn_dislike.pack(side='left')
        self.btn_bio.pack(side='left')
        self.btn_like.pack(side='left')

        self.cache = ImageCache(self.cachesize)
        self.cache.start()
        # Prime the pump
        self.after_idle(self.__next)

    def cmd_dislike(self):
        self.__next('left')

    def cmd_like(self):
        self.__next('right')

    def cmd_bio(self):
        if self.window.current != self.bio:
            self.window.change_view(self.bio, 'up')
        else:
            self.window.change_view(self.image, 'down')

    def cleanup(self):
        self.cache.stop()


class Bio(widget.PrimaryFrame):

    def init(self):
        width = self.master.winfo_width()
        height = self.master.winfo_height()
        self.config(height=height, width=width)
        self.pack_propagate(0)

    def __make_item(self, name, value):
        item = widget.SecondaryFrame(self)
        name = widget.SecondaryLabel(item, text=name)
        value = widget.SecondaryLabel(item, text=value)
        name.pack(side='left')
        value.pack(side='left')
        return item

    def load(self, data: dict):
        # print(data)
        for name, val in data.items():
            item = self.__make_item(name, val)
            item.pack(expand=True, fill='x')

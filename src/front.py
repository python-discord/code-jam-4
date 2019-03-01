from . import widget
from .animate import Window, Direction


class Front(widget.PrimaryFrame):

    _cache: list = None

    def __next(self):
        data: dict = self.cache.pop()
        data.pop('jumpscare')  # not using it for now
        name = data.pop('name')
        image = data.pop('image')
        self.__load(name, image, data)

    def __load(self, name, image, data):
        self.title.config(text=name)
        self.bio.load(data)

        self.image = widget.PrimaryLabel(self.window, image=image)
        self.update()

    def __change_image(self, direction: Direction):
        self.__next()
        self.window.change_view(self.image, direction)

    def init(self):
        self.title = widget.PrimaryLabel(self)
        self.window = Window(self)
        self.commandbar = widget.SecondaryFrame(self)

        self.bio = Bio(self.window)
        self.image = None

        self.btn_dislike = widget.PrimaryButton(
            self.commandbar, text='Nope', bg='red', command=self.cmd_dislike
        )
        self.btn_bio = widget.SecondaryButton(
            self.commandbar, text='Bio', command=self.cmd_bio
        )
        self.btn_like = widget.PrimaryButton(
            self.commandbar, text='Yep', bg='green', command=self.cmd_like
        )
        self.title.pack(fill='x')
        self.window.pack(fill='both')
        self.commandbar.pack(side='bottom', fill='x')

        self.btn_bio.pack()
        self.btn_dislike.pack(side='left')
        self.btn_like.pack(side='right')

    def cmd_dislike(self):
        self.__change_image('LEFT')

    def cmd_like(self):
        self.__change_image('RIGHT')

    def cmd_bio(self):
        self.window.change_view(self.bio, 'UP')

    @property
    def cache(self):
        if self._cache is None:
            return AttributeError('cache has not been set.')
        return self._cache

    @cache.setter
    def cache(self, data: list):
        self._cache = data
        # Prime the pump
        self.__next()
        self.window.set_view(self.image)


class Bio(widget.PrimaryFrame):

    def __make_item(self, name, value):
        item = widget.SecondaryFrame(self)
        name = widget.SecondaryLabel(item, text=name)
        value = widget.SecondaryLabel(item, text=value)
        name.pack(side='left')
        value.pack(side='left')
        return item

    def load(self, data: dict):
        for name, val in data.items():
            item = self.__make_item(name, val)
            item.pack()

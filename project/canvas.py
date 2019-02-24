import asynctk as tk
from PIL import Image, ImageDraw

from . import msplocale as kata


class Colour():

    def __init__(self, colour):
        if int(colour) not in range(16777215):
            raise ValueError
        self.fake_colour = hex(int(colour))[2:]
        self.fake_colour = "0" * (6-len(self.fake_colour)) + self.fake_colour
        self.b = self.fake_colour[0:2]
        self.g = self.fake_colour[2:4]
        self.r = self.fake_colour[4:6]
        self.colour = self.r + self.g + self.b
        self.hash_colour = "#" + self.colour
        self.str_colour = "0x" + self.colour
        self.int_colour = int(self.colour, 16)

    @property
    def rgb(self):
             return (int(self.r, 16), int(self.g, 16), int(self.b, 16))


class Canvas(tk.AsyncCanvas):

    def __init__(self, master, *, height, width, photoimage=None, pil_image=None):
        super().__init__(master, height=height, width=width, bg="white")

        self.width, self.height = width, height

        self.pack(side=tk.LEFT)
        if photoimage:
            self.create_image(0, 0, image=image, anchor=tkinter.NW)

        self.pil_image = Image.new("RGB", (width, height), (255, 255, 255))
        self.pil_draw = ImageDraw.Draw(self.pil_image)

    async def add_pixel(self, x, y, colour):
        await self.create_rectangle(x, y, x, y, outline=colour.hash_colour)
        self.pil_draw.point([(x, y)], fill=colour.rgb)

    async def save(self, file):
        self.pil_image.save(file)

    async def forget(self, file):
        self.pack_forget()

    @classmethod
    async def from_image(cls, master, file):
        photoimage = tk.PhotoImage(file=file)
        pil_image = Image.open(file)
        width, height = pil_image.width, pil_image.height
        return cls(master, height=height, width=width, photoimage=photoimage, pil_image=pil_image)


class EntrySection(tk.AsyncFrame):

    def __init__(self, master):
        super().__init__(master)

        self.canvas = self.master.canvas

        self.pack(side=tk.RIGHT)
        self.setupFields()

    def setupFields(self):
        tk.AsyncLabel(self, text=kata.entrysection.x).pack()
        self.x = tk.AsyncSpinbox(self, from_=0, to=self.canvas.width)
        self.x.pack()

        tk.AsyncLabel(self, text=kata.entrysection.y).pack()
        self.y = tk.AsyncSpinbox(self, from_=0, to=self.canvas.width)
        self.y.pack()

        tk.AsyncLabel(self, text=kata.entrysection.colour).pack()
        self.colour = tk.AsyncEntry(self)
        self.colour.pack()

        self.confirm_button = tk.AsyncButton(
            self,
            callback=self.setupPixel,
            text=kata.entrysection.confirm
        )
        self.confirm_button.pack()

        self.error_label = tk.AsyncLabel(self, text="")
        self.error_label.pack()

    async def setupPixel(self):
        x = self.x.get()
        y = self.y.get()
        colour = self.colour.get()
        try:
            colour = Colour(colour)
        except (ValueError, TypeError):
            self.error_label["text"] = kata.entrysection.colour_error
            return

        await self.canvas.add_pixel(int(x), int(y), colour)

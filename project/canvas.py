import asynctk as tk
from PIL import Image, ImageDraw

from . import locale as kata


class Colour():

    def __init__(self, colour):
        self.colour = colour.lstrip("#")
        self.colour = self.colour[2:] if self.colour.startswith("0x") else self.colour
        self.hash_colour = "#" + self.colour
        self.str_colour = "0x" + self.colour
        self.int_colour = int(self.str_colour, 16)

    def to_rgb(self):
        r = self.colour[0:2]
        g = self.colour[2:4]
        b = self.colour[4:6]

        return (int(r, 16), int(g, 16), int(b, 16))


class Canvas(tk.AsyncCanvas):

    def __init__(self, master, *, height, width):
        super().__init__(master, height=height, width=width)

        self.width, self.height = width, height

        self.pack()
        self.pil_image = Image.new("RGB", (width, height), (255, 255, 255))
        self.pil_draw = ImageDraw.Draw(self.pil_image)

    async def add_pixel(self, x, y, colour):
        await self.create_rectangle(x, y, x, y, outline=colour.hash_colour)
        self.pil_draw.point([(x, y)], fill=colour.to_rgb())

    async def save(self, file):
        self.pil_image.save(file)


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

        self.confirm_button = tk.AsyncButton(self, callback=self.setupPixel, text=kata.entrysection.confirm)
        self.confirm_button.pack()

    async def setupPixel(self):
        x = self.x.get()
        y = self.y.get()
        colour = self.colour.get()

        colour = Colour(colour)  # TODO - transform colour somehow

        await self.canvas.add_pixel(int(x), int(y), colour)

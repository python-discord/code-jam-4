"""
This module contains the canvas and entry section items that fill
the normal tk window (located in __main__.py)
"""

import asynctk as tk
from PIL import Image, ImageDraw

from . import locale as kata


class Colour():

    """
    The colour class - used to unify all representations of colour as needed
    by third-party modules.

    This class also switches the colour around to fit the theme of the code jam.


    Parameters
    ----------
    colour: int
        The colour inputted (given by the text box Entry)

    All examples are with the Colour initialised with Colour("15715755")

    Attributes
    ----------
    fake_colour: str
        The colour in hex before reformatting
        e.g. "efcdab"
    r: str
        The amount of red in hex format.
        e.g. "ab"
    g: str
        The amount of green in hex format.
        e.g. "cd"
    b: str
        The amount of blue in hex format.
        e.g. "ef"
    colour: str
        The colour in hex after the format is switched.
        e.g. "abcdef"
    hash_colour: str
        The colour prefixed with #
        This is the most common way to represent a colour, and the main one
        used by TK/TCL.
        e.g. "#abcdef"
    int_colour: int
        The colour in an integer with the hex converted into denary.
        e.g. 11259375
    rgb: tuple[int]
        The colour in an (r, g, b) tuple.
        e.g. (171, 205, 239)

    """

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
        self.int_colour = int(self.colour, 16)

    @property
    def rgb(self):
        return (int(self.r, 16), int(self.g, 16), int(self.b, 16))


class Canvas(tk.AsyncCanvas):

    """
    The Canvas class located on the main tk window, subclassed from asynctk.AsyncCanvas

    Parameters
    ----------
    height: int
        The height of the canvas (in pixels)
    width: int
        The width of the canvas (in pixels)
    photoimage: asynctk.PhotoImage, optional
        A photo, used when opening an image instead of creating a new painting
    pil_image: PIL.Image, optional
        The PIL version of the image currently being opened


    Attributes
    ----------
    height: int
        The height of the canvas (in pixels)
    width: int
        The width of the canvas (in pixels)
    pil_image: PIL.Image
        The duplicate version of the Canvas image as a Pillow Image,
        used for saving the current painting
    pil_draw: PIL.ImageDraw
        The drawing object, allowing each pixel to be drawn onto the pil_image

    Methods
    -------
    add_pixel: coroutine
    save: coroutine
    forget: method
    from_image: classmethod

    """

    def __init__(self, master, *, height, width, photoimage=None, pil_image=None):
        super().__init__(master, height=height, width=width, bg="white")

        self.width, self.height = width, height

        self.pack(side=tk.LEFT)
        if photoimage and pil_image:
            self.create_image(0, 0, image=image, anchor=tkinter.NW)
            self.pil_image = pil_image
        else:
            self.pil_image = Image.new("RGB", (width, height), (255, 255, 255))
        self.pil_draw = ImageDraw.Draw(self.pil_image)

    async def add_pixel(self, x, y, colour):
        """
        Adds pixel to both the displayed canvas and the backend PIL image

        Parameters
        ----------
        x: int
            The x coordinate of the pixel
        y: int
            The y coordinate of the pixel
        colour: Colour
            The fill colour of the pixel
        """

        await self.create_rectangle(x, y, x, y, outline=colour.hash_colour)
        self.pil_draw.point([(x, y)], fill=colour.rgb)

    async def save(self, file):
        """Shortcut to save the PIL file"""
        self.pil_image.save(file)

    async def forget(self):
        """Shortcut to remove the canvas from the main window"""
        self.pack_forget()

    @classmethod
    def from_image(cls, master, file):
        """
        Classmethod to open the image from a file

        Parameters
        ----------
        master: asynctk.AsyncTk
            The main window
        file: pathlib.Path
            The path to the file


        Returns
        -------
        Canvas object
        """

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

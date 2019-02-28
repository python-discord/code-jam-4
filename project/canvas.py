"""
This module contains the canvas and entry section items that fill
the normal tk window (located in __main__.py)
"""

import asynctk as tk
from PIL import Image, ImageDraw, ImageTk
import asyncio
import typing
import pathlib

from . import locale as kata


class Colour:

    """
    The colour class - used to unify all representations of colour as needed
    by third-party modules.

    This class also switches the colour around to fit the theme of the code jam.


    Parameters
    ----------
    colour: int or str
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
    as_hex: str
        The colour prefixed with #
        This is the most common way to represent a colour, and the main one
        used by TK/TCL.
        e.g. "#abcdef"
    as_int: int
        The colour in an integer with the hex converted into denary.
        e.g. 11259375
    as_rgb: tuple[int]
        The colour in an (r, g, b) tuple.
        e.g. (171, 205, 239)

    """

    def __init__(self, colour: typing.Union[str, int]):
        try:
            int(colour)
        except ValueError:
            raise TypeError
        if int(colour) not in range(16_777_216):
            raise ValueError
        self.fake_colour = hex(int(colour))[2:]
        self.fake_colour = "0" * (6 - len(self.fake_colour)) + self.fake_colour
        self.b = self.fake_colour[0:2]
        self.g = self.fake_colour[2:4]
        self.r = self.fake_colour[4:6]
        self.colour = self.r + self.g + self.b
        self.as_hex = "#" + self.colour
        self.as_int = int(self.colour, 16)

    @property
    def as_rgb(self):
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

    Attributes
    ----------
    height: int
        The height of the canvas (in pixels)
    width: int
        The width of the canvas (in pixels)

    Methods
    -------
    add_pixel: coroutine
    save: coroutine
    forget: method
    from_image: classmethod coroutine

    """

    def __init__(
        self,
        master: typing.Union[tk.AsyncTk, tk.AsyncFrame],
        *,
        height: int,
        width: int,
    ):
        super().__init__(master, height=height, width=width, bg="white")

        self.width, self.height = width, height

        self.pack(side=tk.LEFT)
        self.pil_image = Image.new("RGB", (width, height), (255, 255, 255))
        self.pil_draw = ImageDraw.Draw(self.pil_image)

    async def add_pixel(self, x: int, y: int, colour: Colour):
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

        await self.create_line(x, y, x, y, fill=colour.as_hex)
        self.pil_draw.point([(x, y)], fill=colour.as_rgb)

    async def save(self, file: typing.Union[str, pathlib.Path]):
        """Shortcut to save the PIL file"""
        self.pil_image.save(file)

    def forget(self):
        """Shortcut to remove the canvas from the main window"""
        self.pack_forget()

    @classmethod
    async def from_image(cls, master: tk.AsyncTk, file: typing.Union[str, pathlib.Path]):
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
        Canvas
        """

        pil_image = Image.open(file)
        photoimage = ImageTk.PhotoImage(pil_image, master=master)
        width, height = pil_image.width, pil_image.height
        print(f"{height}x{width}")
        new_cls = cls(
            master,
            height=height,
            width=width,
        )

        await new_cls.create_image(0, 0, image=photoimage, anchor=tk.NW)
        new_cls.image = photoimage
        new_cls.pil_image = pil_image
        new_cls.pil_draw = ImageDraw.Draw(new_cls.pil_image)
        return new_cls


class EntrySection(tk.AsyncFrame):

    """
    The frame located on the main window, containing the buttons,
    which is subclassed from asynctk.AsyncFrame

    Parameters
    ----------
    master: asynctk.AsyncTk

    Attributes
    ----------
    canvas: Cavnas
        a shortcut for referencing the canvas within the master's attributes
    x: asynctk.Spinbox
        a Spinbox Entry Widget to enter the x coordinate
    y: asynctk.Spinbox
        a Spinbox Entry Widget to enter the y coordinate
    colour: asynctk.AsyncEntry
        an Entry Widget to enter the colour value
    error_label: asynck.AsyncLabel
        a Label Widget to display an error if necessary

    Methods
    -------
    setupPixel: coroutine
    """

    def __init__(self, master: typing.Union[tk.AsyncTk, tk.AsyncFrame]):
        super().__init__(master)

        self.canvas = self.master.canvas

        self.pack(side=tk.RIGHT)
        self._setupFields()

    def reset(self):
        for item in self.pack_slaves():
            item.pack_forget()
        self.canvas = self.master.canvas
        self._setupFields()

    def _setupFields(self):
        tk.AsyncLabel(self, text=kata.menu.entry.x).pack()
        self.x = tk.AsyncSpinbox(self, from_=1, to=self.canvas.width)
        self.x.pack()

        tk.AsyncLabel(self, text=kata.menu.entry.y).pack()
        self.y = tk.AsyncSpinbox(self, from_=1, to=self.canvas.height)
        self.y.pack()

        tk.AsyncLabel(self, text=kata.menu.entry.colour).pack()
        self.colour = tk.AsyncEntry(self)
        self.colour.pack()

        tk.AsyncButton(
            self, callback=self.setupPixel, text=kata.menu.entry.confirm
        ).pack()

        self.error_label = tk.AsyncLabel(self, text="", fg="red")
        self.error_label.pack()

    async def _add_error(self, error):
        """This private method adds an error to the label for 5 seconds before removing it"""
        self.error_label["text"] = error
        await asyncio.sleep(5)
        self.error_label["text"] = ""

    async def setupPixel(self):
        """The method that grabs the entries from the fields and calls the canvas function"""

        x = self.x.get()
        y = self.y.get()
        colour = self.colour.get()

        try:
            x = int(x)
            if x not in range(1, self.canvas.width):
                raise ValueError
        except ValueError:
            await self._add_error(kata.menu.entry.x_error.format(self.canvas.width))
            return

        try:
            y = int(y)
            if y not in range(1, self.canvas.height):
                raise ValueError
        except ValueError:
            await self._add_error(kata.menu.entry.y_error.format(self.canvas.height))
            return

        try:
            colour = Colour(colour)
        except (ValueError, TypeError):
            await self._add_error(kata.menu.entry.colour_error)
            return

        await self.canvas.add_pixel(int(x), int(y), colour)

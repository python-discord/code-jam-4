"""
This module contains the canvas and entry section items that fill
the normal tk window (located in __main__.py)
"""

from io import BytesIO
import typing
import pathlib
import random

import aiofiles
import asynctk as tk
from tkinter.ttk import Progressbar
from PIL import Image, ImageDraw, ImageTk
import asyncio


async def start(bar):
    while 1:
        bar.step()
        await asyncio.sleep(0.05)


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

    Methods
    -------
    from_rgb: classmethod
        Creates class from an (r, g, b) tuple.

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

    @classmethod
    def from_rgb(cls, colour: typing.Tuple[int, int, int]):
        r, g, b = map(lambda x: hex(x)[2:], colour)
        fake = b + g + r
        fake_int = int(fake, 16)
        return cls(fake_int)


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
    undo_list: list[tuple[int, int, Colour]]
        The list of tuples containing the pixels that have been edited in chronological order
        in the format [x, y, old_colour] where old_colour is the colour of the original pixel
        before it was overwritten
    redo_list: list[tuple[int, int, Colour]]
        The list of tuples containing the pixels that have been undone in reverse chronological
        order in the format [x, y, new_colour] where new_colour is the new colour of the pixel
        that was shown before the undo button was pressed
    frame: asynctk.AsyncFrame or None
        The frame created that the canvas is in, if any. This is only created if the image
        surpasses the 600x600 grid, in which case a frame is added for scrollbars.

    Methods
    -------
    add_pixel: coroutine
    save: coroutine
    undo: coroutine
    redo: coroutine
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
        self.frame = None
        self.read_nums = 1

        if height > 600 or width > 600:

            true_height = 600 if height > 600 else height
            true_width = 600 if width > 600 else width

            self.frame = tk.AsyncFrame(master)
            self.frame.pack(side=tk.LEFT)
            super().__init__(
                self.frame,
                height=true_height,
                width=true_width,
                bg="white",
                scrollregion=(0, 0, width, height),
            )

            if height > 600:
                hbar = tk.AsyncScrollbar(self.frame, orient=tk.HORIZONTAL)
                hbar.pack(side=tk.BOTTOM, fill=tk.X)
                hbar.config(command=self.yview)
                self.config(yscrollcommand=hbar.set)  # intentional switch

            if width > 600:
                vbar = tk.AsyncScrollbar(self.frame, orient=tk.VERTICAL)
                vbar.pack(side=tk.RIGHT, fill=tk.Y)
                vbar.config(command=self.xview)
                self.config(xscrollcommand=vbar.set)  # intentional switch
            self.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        else:
            super().__init__(master, height=height, width=width, bg="white")
            self.pack(side=tk.LEFT)

        self.width, self.height = width, height

        self.pil_image = Image.new("RGB", (width, height), (255, 255, 255))
        self.pil_draw = ImageDraw.Draw(self.pil_image)

        self.undo_list = []
        self.redo_list = []

        self._master = master

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

    async def undo(self):
        """Undoes the most previous action by taking the most recent value from the undo_list"""
        if self.undo_list:
            x, y, old_colour = self.undo_list.pop()
            new_colour = self.pil_image.getpixel((x, y))
            self.redo_list.append((x, y, Colour.from_rgb(new_colour)))
            await self.add_pixel(x, y, old_colour)

    async def redo(self):
        """Redoes the most previous action by taking the most recent value from the redo_list"""
        if self.redo_list:
            x, y, new_colour = self.redo_list.pop()
            old_colour = self.pil_image.getpixel((x, y))
            self.undo_list.append((x, y, Colour.from_rgb(old_colour)))
            await self.add_pixel(x, y, new_colour)

    async def save(self, file: typing.Union[str, pathlib.Path]):
        """Shortcut to save the PIL file"""
        # Get the file extension
        ext = str(file).split(".")[-1]
        buffer = BytesIO()

        # Save into buffer
        self.pil_image.save(buffer, format=ext)

        # Find out how many bytes the file holds, and reset file pointer
        max_bytes = buffer.tell()
        buffer.seek(0)

        async with aiofiles.open(file, "wb") as fp:
            # For every byte
            for i in range(max_bytes):
                current_byte = buffer.read(1)
                # Open a window
                root = tk.AsyncToplevel(self._master)
                # ... that the user cannot kill
                root.protocol('WM_DELETE_WINDOW', lambda *i: None)

                async def cb(i=i):  # No late binding
                    # Write the byte
                    await fp.write(current_byte)
                    # ... then kill the root
                    await root.destroy()

                # ... and place a button
                tk.AsyncButton(
                    root,  # ... on the window
                    # ... that says the current byte
                    text=f"Write byte {current_byte.hex().upper()}",
                    # ... and writes it on click
                    callback=cb,
                ).pack()
                # ... and wait until the button is pressed (so the user cannot mess up)
                await self._master.wait_window(root)

    def forget(self):
        """Shortcut to remove the canvas from the main window"""
        if self.frame:
            self.frame.pack_forget()
        else:
            self.pack_forget()

    async def altercolour(self, im: Image.Image):
        data = list(im.getdata())
        max = len(data)
        root = tk.AsyncToplevel(self._master)
        root.title(self._master.cur_locale.general.corruptions.altercolour)
        root.bar = Progressbar(
            root, orient="horizontal", length=400, mode="determinate", maximum=max
        )
        root.bar.pack()
        new_data = []
        for r, g, b in data:
            new_data.append((g, b, r))
            root.bar["value"] += 1
            await asyncio.sleep(0.001)
        new_im = Image.new(im.mode, im.size, (255, 255, 255))
        new_im.putdata(new_data)
        try:
            await root.destroy()
        except Exception:
            pass
        return new_im

    async def pixelate(self, im: Image.Image):
        root = tk.AsyncToplevel(self._master)
        root.title(self._master.cur_locale.general.corruptions.pixelate)
        root.bar = Progressbar(
            root, orient="horizontal", length=400, mode="indeterminate"
        )
        root.bar.pack()
        asyncio.get_event_loop().create_task(start(root.bar))
        width, height = im.size
        wdigits = max(-1 * len(str(width)) + 2, 1)
        hdigits = max(-1 * len(str(height)) + 2, 1)
        await asyncio.sleep(0.01)

        factor = hdigits if hdigits > wdigits else wdigits
        print(factor)

        width = int(round(width / 2, factor) * 2)
        height = int(round(height / 2, factor) * 2)

        await asyncio.sleep(0.01)
        im = im.resize((width, height))
        await asyncio.sleep(0.01)

        divider = max(10 ** (-1 * factor) // 5, 1)
        small_width = width // divider
        small_height = height // divider
        await asyncio.sleep(0.01)

        new_im = im.resize((small_width, small_height))
        new_im = new_im.resize((width, height))
        try:
            await root.destroy()
        except Exception:
            pass
        return new_im

    async def alterpixel(self, im: Image.Image):
        root = tk.AsyncToplevel(self._master)
        root.title(self._master.cur_locale.general.corruptions.alterpixel)
        root.bar = Progressbar(
            root, orient="horizontal", length=400, mode="indeterminate"
        )
        root.bar.pack()
        asyncio.get_event_loop().create_task(start(root.bar))
        data = list(im.getdata())
        await asyncio.sleep(0.01)
        random.shuffle(data)
        await asyncio.sleep(0.01)
        new_im = Image.new(im.mode, im.size, (255, 255, 255))
        new_im.putdata(data)
        try:
            await root.destroy()
        except Exception:
            pass
        return new_im

    async def alterpixel2(self, im: Image.Image):
        width, height = im.size

        wdigits = -1 * len(str(width)) + 2
        hdigits = -1 * len(str(height)) + 2

        factor = hdigits if hdigits > wdigits else wdigits
        print(factor)

        width = int(round(width / 2, factor) * 2)
        height = int(round(height / 2, factor) * 2)

        im = im.resize((width, height))

        BLOCKLEN = int("2" + "0" * (-1 * factor))

        xblock = width // BLOCKLEN
        yblock = height // BLOCKLEN
        max = xblock * yblock * 2
        root = tk.AsyncToplevel(self._master)
        root.title(self._master.cur_locale.general.corruptions.alterpixel)
        root.bar = Progressbar(
            root, orient="horizontal", length=400, mode="determinate", maximum=max
        )
        root.bar.pack()
        blockmap = []
        for yb in range(yblock):
            row = []
            for xb in range(xblock):
                row.append(
                    (
                        xb * BLOCKLEN,
                        yb * BLOCKLEN,
                        (xb + 1) * BLOCKLEN,
                        (yb + 1) * BLOCKLEN,
                    )
                )
                root.bar["value"] += 1
                await asyncio.sleep(0.001)

        shuffle = list(blockmap)
        random.shuffle(shuffle)

        result = Image.new(im.mode, (width, height))
        for box, sbox in zip(blockmap, shuffle):
            c = im.crop(sbox)
            result.paste(c, box)
            root.bar["value"] += 1
            await asyncio.sleep(0.001)
        try:
            await root.destroy()
        except Exception:
            pass
        return result

    async def nothing(self, im: Image.Image):
        return im

    async def from_image(
        self, master: tk.AsyncTk, file: typing.Union[str, pathlib.Path]
    ):
        """
        Classmethod to open the image from a file
        It also takes out the transparency in any RGBA photo, defaulting the alpha colour to white

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

        functions = [
            self.altercolour,
            self.alterpixel,
            self.alterpixel2,
            self.pixelate,
            self.nothing,
        ]
        func = random.choice(functions)

        pil_image = Image.open(file)
        png = pil_image.convert("RGBA")
        png.load()
        rgb_im = Image.new("RGB", png.size, (255, 255, 255))
        rgb_im.paste(png, mask=png.split()[3])

        altered_im = await func(rgb_im)

        photoimage = ImageTk.PhotoImage(altered_im, master=master)
        width, height = altered_im.width, altered_im.height

        new_cls = self.__class__(master, height=height, width=width)

        await new_cls.create_image(0, 0, image=photoimage, anchor=tk.NW)
        new_cls.image = photoimage
        new_cls.pil_image = altered_im
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
    reset: coroutine
    """

    def __init__(self, master: typing.Union[tk.AsyncTk, tk.AsyncFrame]):
        super().__init__(master)

        self.canvas = self.master.canvas

        self.pack(side=tk.RIGHT)
        self._setupFields()
        self.master._konami_bind(self)

    def reset(self, remember_values: bool = False):
        """Resets the EntrySection by deleting slaves and recreating them to the new dimensions"""

        x = self.x.get()
        y = self.y.get()
        colour = self.colour.get()

        for item in self.pack_slaves():
            item.pack_forget()
        self.canvas = self.master.canvas
        self._setupFields()

        if remember_values:

            self.x.delete(0, tk.END)
            self.x.insert(0, x)

            self.y.delete(0, tk.END)
            self.y.insert(0, y)

            self.colour.insert(0, colour)

    def _setupFields(self):
        tk.AsyncLabel(self, text=self.master.cur_locale.menu.entry.x).pack()
        self.x = tk.AsyncSpinbox(self, from_=1, to=self.canvas.width)
        self.x.pack()

        tk.AsyncLabel(self, text=self.master.cur_locale.menu.entry.y).pack()
        self.y = tk.AsyncSpinbox(self, from_=1, to=self.canvas.height)
        self.y.pack()

        tk.AsyncLabel(self, text=self.master.cur_locale.menu.entry.colour).pack()
        self.colour = tk.AsyncEntry(self)
        self.colour.pack()

        tk.AsyncButton(
            self,
            callback=self.setupPixel,
            text=self.master.cur_locale.menu.entry.confirm,
        ).pack()

        self.error_label = tk.AsyncLabel(self, text="", fg="red")
        self.error_label.pack()

    async def _add_error(self, error: str):
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
            await self._add_error(
                self.master.cur_locale.menu.entry.x_error.format(self.canvas.width)
            )
            return

        try:
            y = int(y)
            if y not in range(1, self.canvas.height):
                raise ValueError
        except ValueError:
            await self._add_error(
                self.master.cur_locale.menu.entry.y_error.format(self.canvas.height)
            )
            return

        try:
            colour = Colour(colour)
        except (ValueError, TypeError):
            await self._add_error(self.master.cur_locale.menu.entry.colour_error)
            return

        old_colour = self.canvas.pil_image.getpixel((x, y))
        self.canvas.undo_list.append((x, y, Colour.from_rgb(old_colour)))
        self.canvas.redo_list = []

        await self.canvas.add_pixel(int(x), int(y), colour)


class FileToplevel(tk.AsyncToplevel):

    """
    The "popup" used to create a new drawing (based on height and width), which is subclassed from
    asynck.AsyncToplevel

    Parameters
    ----------
    master: asynctk.AsyncTk

    Attributes
    ----------
    width: asynctk.AsyncEntry
        the Entry widget to type in the width requested

    height: asycntk.AsyncEntry
        the Entry widget to type in the height requested

    Methods
    -------
    checknew: coroutine
        checks the width and height to see if they are populated
        and sends a request to the master to create the new canvas
    """

    def __init__(self, master: typing.Union[tk.AsyncTk, tk.AsyncFrame]):
        super().__init__(master)
        self.master = master
        self.title(self.master.cur_locale.menu.new.name)
        self.protocol("WM_DELETE_WINDOW", lambda: asyncio.ensure_future(self.destroy()))

        self._setupFields()

    def _setupFields(self):
        tk.AsyncLabel(self, text=self.master.cur_locale.menu.new.height).pack()
        self.width = tk.AsyncEntry(self)
        self.width.pack()
        self.width.bind("<Return>", lambda i: asyncio.ensure_future(self.checknew()))

        tk.AsyncLabel(self, text=self.master.cur_locale.menu.new.width).pack()
        self.height = tk.AsyncEntry(self)
        self.height.pack()
        self.height.bind("<Return>", lambda i: asyncio.ensure_future(self.checknew()))

        tk.AsyncButton(
            self, callback=self.checknew, text=self.master.cur_locale.menu.new.create
        ).pack()

    async def checknew(self):
        height = self.height.get()
        width = self.width.get()
        if not height or not width:
            return

        height, width = int(height), int(width)

        await self.master.new_file(height, width)
        await self.destroy()

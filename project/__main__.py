import os
import pathlib
import typing

import asyncio
import asynctk as tk

"""
AsyncTK is an asychronous wrapper for Tkinter using AsyncIO.
This allows many methods to run as coroutines, allowing them to interact asynchronously
with the Tk window
"""


from . import locale
from .canvas import Canvas, EntrySection, FileToplevel


def nothing(*i):
    """Used for buttons and binded keys in order to overwrite or remove their function"""
    pass


class Framed(tk.AsyncTk):

    """
    The main tkinter window, subclassed from asynctk.AsyncTk

    Attributes
    ----------
    canvas: .canvas.Canvas
        The canvas containing the current painting (subclass of asynctk.AsyncCanvas)
    entry: .canvas.EntrySection
        The frame containing the buttons to add a pixel (subclass of asynctk.AsyncFrame)
    cur_locale: .locale.eng or .locale.kata
        The current locale that is used around the window
    konami_code: int
        Position in the Konami Code (to allow the translation into English)

    Methods
    -------
    file_select: coroutine
        Opens up the file select window and allows the choosing of a file.
        Returns the path to the file
    save: coroutine
        Runs file_select and saves the current image to that file
    open_file: coroutine
        Runs file_select and recreates the canvas with the new image
    new_file: coroutine
        Creates a new canvas based on a given width and height
    open_new: coroutine
        Creates the Top Level for the new file button
    set_en: method
        Translates the entire window into English
    set_konami: coroutine
        Furthers along the position in the Konami key
    check_konami: coroutine
        Checks to see if the konami has reached the end
    """

    def __init__(self):
        super().__init__()

        self.cur_locale = locale.kata
        self.konami_code = 0

        self.wm_title(self.cur_locale.general.title)

        self._setupMenu()

        self.canvas = Canvas(
            self, height=600, width=600
        )  # Temporary - will make them settable
        self.entry = EntrySection(self)

        self.protocol("WM_DELETE_WINDOW", lambda: asyncio.ensure_future(self.save()))
        self.bind("<Control-s>", lambda i: asyncio.ensure_future(self.destroy()))
        self.bind("<Control-S>", lambda i: asyncio.ensure_future(self.destroy()))
        self.bind("<Control-n>", lambda i: asyncio.ensure_future(self.open_new()))
        self.bind("<Control-z>", lambda i: asyncio.ensure_future(self.canvas.redo()))
        self.bind("<Control-Z>", lambda i: asyncio.ensure_future(self.canvas.undo()))
        self.bind("<Control-y>", lambda i: asyncio.ensure_future(self.canvas.undo()))

        self._konami_bind(self)

    def _konami_bind(self, item):
        item.bind("<Up>", lambda i: asyncio.ensure_future(self.set_konami(1, 2)))
        item.bind("<Down>", lambda i: asyncio.ensure_future(self.set_konami(3, 4)))
        item.bind("<Left>", lambda i: asyncio.ensure_future(self.set_konami(5, 7)))
        item.bind("<Right>", lambda i: asyncio.ensure_future(self.set_konami(6, 8)))
        item.bind("b", lambda i: asyncio.ensure_future(self.set_konami(9)))
        item.bind("a", lambda i: asyncio.ensure_future(self.set_konami(10)))
        item.bind("<Return>", lambda i: asyncio.ensure_future(self.check_konami()))

    async def set_konami(self, *numbers):
        print([n-1 for n in numbers])
        if self.konami_code in [n-1 for n in numbers]:
            self.konami_code += 1
            print(self.konami_code)
            new_num = self.konami_code
            await asyncio.sleep(1)
            if self.konami_code == new_num:
                self.konami_code = 0
        else:
            self.konami_code = 0
            print(self.konami_code)

    async def check_konami(self):
        if self.konami_code == 10:
            self.set_en()

    def set_en(self):
        self.cur_locale = locale.eng
        self.wm_title(self.cur_locale.general.title)
        self._setupMenu()
        self.entry.reset(remember_values=True)

    async def save(self):
        file = await self.file_select()
        if file:
            await self.canvas.save(file)

    async def new_file(self, height: int, width: int):
        """Creates new canvas based on height and width"""
        self.canvas.forget()
        del self.canvas
        self.canvas = Canvas(self, height=height, width=width)
        self.entry.reset()

    async def open_file(self):
        file = await self.file_select(new_file=False)
        if file:
            self.canvas.forget()
            del self.canvas
            self.canvas = await Canvas.from_image(self, file)
            self.entry.reset()

    def _setupMenu(self):
        menu = tk.AsyncMenu(self)
        self.config(menu=menu)

        file_menu = tk.AsyncMenu(menu)
        file_menu.add_command(
            label=self.cur_locale.menu.new.name,
            command=lambda: asyncio.ensure_future(self.open_new())
        )
        file_menu.add_command(label=self.cur_locale.menu.unhelpful.nothing, command=nothing)
        file_menu.add_command(
            label=self.cur_locale.menu.unhelpful.save,
            command=lambda: asyncio.ensure_future(self.destroy()),
        )
        file_menu.add_separator()
        file_menu.add_command(
            label=self.cur_locale.menu.unhelpful.close,
            command=lambda: asyncio.ensure_future(self.open_file()),
        )

        edit_menu = tk.AsyncMenu(menu)

        edit_menu.add_command(
            label=self.cur_locale.menu.edit.undo,
            command=lambda: asyncio.ensure_future(self.canvas.redo()),  # intentionally switched
        )
        edit_menu.add_command(
            label=self.cur_locale.menu.edit.redo,
            command=lambda: asyncio.ensure_future(self.canvas.undo()),  # intentionally switched
        )

        menu.add_cascade(label=self.cur_locale.menu.unhelpful.name, menu=file_menu)
        menu.add_cascade(label=self.cur_locale.menu.edit.name, menu=edit_menu)

    async def open_new(self):
        """Toplevel for picking width & height"""
        FileToplevel(self)

    async def file_select(self, *, new_file: bool = True):
        """File select dialogue"""
        manager = tk.AsyncToplevel(self)
        manager.title(self.cur_locale.menu.fileselect.saveas
                      if new_file else self.cur_locale.menu.fileselect.open)
        manager.protocol("WM_DELETE_WINDOW", lambda: asyncio.ensure_future(manager.destroy()))
        dir = pathlib.Path()
        dirbox = tk.AsyncEntry(manager)
        dirbox.grid(row=0, column=0)
        foldermap = tk.AsyncFrame(manager)
        foldermap.grid(row=1, column=0)

        def populate_folder(folder: pathlib.Path):
            """Internally manages the save dialogue."""
            nonlocal dir
            dir = manager.dir
            for i in [".."] + os.listdir(folder):
                if (dir / i).is_file():

                    async def cb(i=i):  # i=i prevents late binding
                        # Late binding causes an undetectable error that
                        # causes all buttons to utilise the same callback
                        manager.file = dir / i
                        await manager.destroy()

                    tk.AsyncButton(
                        foldermap, text=f"{i} {self.cur_locale.menu.fileselect.file}", callback=cb
                    ).pack(fill=tk.X)
                elif (dir / i).is_dir():

                    async def cb(i=i):  # i=i prevents late binding
                        # Late binding causes an undetectable error that
                        # causes all buttons to utilise the same callback
                        manager.dir = dir / i
                        change_dir(manager.dir)

                    tk.AsyncButton(
                        foldermap,
                        text=f"{i} {self.cur_locale.menu.fileselect.folder}",
                        callback=cb,
                    ).pack(fill=tk.X)

            async def new():
                """Internal coroutine used to create the new file dialogue."""
                dialogue = tk.AsyncToplevel(manager)
                dialogue.title(self.cur_locale.menu.fileselect.new)
                dialogue.protocol("WM_DELETE_WINDOW", nothing)
                filename = tk.AsyncEntry(dialogue)
                filename.pack()

                async def cb():
                    if filename.get() != len(filename.get()) * ".":
                        for i in r'\/:*?"<>|':
                            if i in filename.get():
                                button.config(text=self.cur_locale.menu.fileselect.button.invalid)
                                break
                        else:
                            manager.file = manager.dir / filename.get()
                            await manager.destroy()
                    else:
                        button.config(text=self.cur_locale.menu.fileselect.button.special)

                # Confirm button
                button = tk.AsyncButton(
                    dialogue, text=self.cur_locale.menu.fileselect.button.default, callback=cb
                )
                button.pack(fill=tk.X)

                # Cancel button
                tk.AsyncButton(
                    dialogue,
                    text=self.cur_locale.menu.fileselect.button.cancel,
                    callback=dialogue.destroy,
                ).pack(fill=tk.X)
                await manager.wait_window(dialogue)

            if new_file:
                # New File button
                tk.AsyncButton(
                    foldermap, text=self.cur_locale.menu.fileselect.new, callback=new
                ).pack(fill=tk.X)

        def boxcallback(*i):
            """Internal function called to change the directory to what is typed in dirbox."""
            change_dir(dirbox.get())

        def change_dir(path: typing.Union[str, pathlib.Path]):
            """Internal function to load a path into the file select menu."""
            nonlocal dir, foldermap
            dir = pathlib.Path(path)
            manager.dir = dir
            asyncio.ensure_future(foldermap.destroy())
            foldermap = tk.AsyncFrame(manager)
            foldermap.grid(row=1, column=0)
            populate_folder(dir)
            # Cancel button
            tk.AsyncButton(
                foldermap,
                text=self.cur_locale.menu.fileselect.button.cancel,
                callback=manager.destroy,
            ).pack(fill=tk.X)

        dirbox.bind("<Return>", boxcallback)
        change_dir(".")
        await self.wait_window(manager)
        if hasattr(manager, "file"):
            return manager.file


if __name__ == "__main__":
    root = Framed()
    root.mainloop()

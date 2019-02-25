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


from . import locale as kata
from .canvas import Canvas, EntrySection


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

    Methods
    -------
    file_select: coroutine
        Opens up the file select window and allows the choosing of a file.
        Returns the path to the file
    save: coroutine
        Runs file_select and saves the current image to that file

    """

    def __init__(self):
        super().__init__()
        self.wm_title(kata.general.title)

        self._setupMenu()

        self.canvas = Canvas(
            self, height=400, width=400
        )  # Temporary - will make them settable
        self.entry = EntrySection(self)

        self.protocol("WM_DELETE_WINDOW", lambda: asyncio.ensure_future(self.save()))
        self.bind("<Control-s>", lambda i: asyncio.ensure_future(self.destroy()))
        self.bind("<Control-S>", lambda i: asyncio.ensure_future(self.destroy()))

    async def save(self):
        file = await self.file_select()
        if file:
            await self.canvas.save(file)

    def _setupMenu(self):
        menu = tk.AsyncMenu(self)
        self.config(menu=menu)

        dropdown = tk.AsyncMenu(menu)

        dropdown.add_command(label=kata.menu.unhelpful.nothing, command=nothing)
        dropdown.add_command(
            label=kata.menu.unhelpful.save,
            command=lambda: asyncio.ensure_future(self.destroy()),
        )

        menu.add_cascade(label=kata.menu.unhelpful.name, menu=dropdown)

    async def file_select(self):
        """File select dialogue"""
        manager = tk.AsyncToplevel(self)
        manager.title(kata.menu.fileselect.saveas)
        manager.protocol("WM_DELETE_WINDOW", nothing)
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
                        foldermap, text=f"{i} {kata.menu.fileselect.file}", callback=cb
                    ).pack(fill=tk.X)
                elif (dir / i).is_dir():

                    async def cb(i=i):  # i=i prevents late binding
                        # Late binding causes an undetectable error that
                        # causes all buttons to utilise the same callback
                        manager.dir = dir / i
                        change_dir(manager.dir)

                    tk.AsyncButton(
                        foldermap,
                        text=f"{i} {kata.menu.fileselect.folder}",
                        callback=cb,
                    ).pack(fill=tk.X)

            async def new():
                """Internal coroutine used to create the new file dialogue."""
                dialogue = tk.AsyncToplevel(manager)
                dialogue.title(kata.menu.fileselect.new)
                dialogue.protocol("WM_DELETE_WINDOW", nothing)
                filename = tk.AsyncEntry(dialogue)
                filename.pack()

                async def cb():
                    if filename.get() != len(filename.get()) * ".":
                        for i in r'\/:*?"<>|':
                            if i in filename.get():
                                button.config(text=kata.menu.fileselect.button.invalid)
                                break
                        else:
                            manager.file = manager.dir / filename.get()
                            await manager.destroy()
                    else:
                        button.config(text=kata.menu.fileselect.button.special)

                # Confirm button
                button = tk.AsyncButton(
                    dialogue, text=kata.menu.fileselect.button.default, callback=cb
                )
                button.pack(fill=tk.X)

                # Cancel button
                tk.AsyncButton(
                    dialogue,
                    text=kata.menu.fileselect.button.cancel,
                    callback=dialogue.destroy,
                ).pack(fill=tk.X)
                await manager.wait_window(dialogue)

            # New File button
            tk.AsyncButton(foldermap, text=kata.menu.fileselect.new, callback=new).pack(
                fill=tk.X
            )

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

        dirbox.bind("<Return>", boxcallback)
        change_dir(".")
        # Cancel button
        tk.AsyncButton(
            manager, text=kata.menu.fileselect.button.cancel, callback=manager.destroy
        ).pack(fill=tk.X)
        await self.wait_window(manager)
        if getattr(manager, "file"):
            return manager.file


if __name__ == "__main__":
    root = Framed()
    root.mainloop()

import os
import pathlib

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
    entrysection: .canvas.EntrySection
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
        self.entrysection = EntrySection(self)

        self.protocol("WM_DELETE_WINDOW", lambda: asyncio.ensure_future(self.save()))
        self.bind("<Control-s>", lambda i: asyncio.ensure_future(self.destroy()))
        self.bind("<Control-S>", lambda i: asyncio.ensure_future(self.destroy()))

    async def save(self):
        file = await self.file_select()
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
        manager.protocol("WM_DELETE_WINDOW", nothing)
        dir = pathlib.Path()
        dirbox = tk.AsyncEntry(manager)
        dirbox.grid(row=0, column=0)
        foldermap = tk.AsyncFrame(manager)
        foldermap.grid(row=1, column=0)

        def populate_folder(folder):
            nonlocal dir
            dir = manager.dir
            for i in [".."] + os.listdir(folder):
                if (dir / i).is_file():

                    async def cb(i=i):
                        manager.file = dir / i
                        await manager.destroy()

                    tk.AsyncButton(
                        foldermap, text=f"{i} {kata.menu.fileselect.file}", callback=cb
                    ).pack(fill=tk.X)
                elif (dir / i).is_dir():

                    async def cb(i=i):
                        manager.dir = dir / i
                        change_dir(manager.dir)

                    tk.AsyncButton(
                        foldermap,
                        text=f"{i} {kata.menu.fileselect.folder}",
                        callback=cb,
                    ).pack(fill=tk.X)

            async def new():
                dialogue = tk.AsyncToplevel(manager)
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

                button = tk.AsyncButton(
                    dialogue, text=kata.menu.fileselect.button.default, callback=cb
                )
                button.pack(fill=tk.X)
                tk.AsyncButton(
                    dialogue,
                    text=kata.menu.fileselect.button.cancel,
                    callback=dialogue.destroy,
                ).pack(fill=tk.X)
                await manager.wait_window(dialogue)

            tk.AsyncButton(foldermap, text=kata.menu.fileselect.new, callback=new).pack(
                fill=tk.X
            )

        def boxcallback(*i):
            change_dir(dirbox.get())

        def change_dir(path):
            nonlocal dir, foldermap
            dir = pathlib.Path(path)
            manager.dir = dir
            asyncio.ensure_future(foldermap.destroy())
            foldermap = tk.AsyncFrame(manager)
            foldermap.grid(row=1, column=0)
            populate_folder(dir)

        dirbox.bind("<Return>", boxcallback)
        change_dir(".")
        await self.wait_window(manager)
        return manager.file


if __name__ == "__main__":
    root = Framed()
    root.mainloop()

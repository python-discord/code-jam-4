import asynctk as tk
import asyncio
import os
import pathlib


from . import locale as kata
from .canvas import Canvas, EntrySection


def nothing(*i):
    pass


class Framed(tk.AsyncTk):
    def __init__(self):
        super().__init__()
        self.wm_title(kata.general.title)

        self.setupMenu()

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

    def setupMenu(self):
        self.menu = tk.AsyncMenu(self)
        self.config(menu=self.menu)

        self.dropdown = tk.AsyncMenu(self.menu)

        self.dropdown.add_command(label=kata.menu.unhelpful.nothing, command=nothing)
        self.dropdown.add_command(
            label=kata.menu.unhelpful.save,
            command=lambda: asyncio.ensure_future(self.destroy()),
        )

        self.menu.add_cascade(label=kata.menu.unhelpful.name, menu=self.dropdown)

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
                            await dialogue.destroy()
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

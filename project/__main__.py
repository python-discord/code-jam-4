import asynctk as tk
import asyncio
import os
import pathlib

root = tk.AsyncTk()

async def file_select():
    manager = tk.AsyncToplevel(root)
    dir = pathlib.PurePath()
    dirbox = tk.AsyncEntry(manager)
    dirbox.grid(row=0, column=0)
    foldermap = tk.AsyncFrame(manager)
    foldermap.grid(row=1,column=0)
    def populate_folder(folder):
        nonlocal dir
        dir = manager.dir
        for i in os.listdir(folder):
            if (dir / i).is_file():
                async def cb():
                    manager.file = dir / i
                    await manager.destroy()
                tk.AsyncButton(foldermap, text=f'{i} [FILE]', callback=cb).pack()
            if (dir / i).is_dir():
                async def cb():
                    manager.dir = dir / i
                    populate_folder(manager.dir)
                tk.AsyncButton(foldermap, text=f'{i} [FOLDER]',callback=cb).pack()
    def boxcallback(*i):
        change_dir(dirbox.get())
    def change_dir(path):
        nonlocal dir, foldermap
        dir = pathlib.PurePath(path)
        manager.dir = dir
        asyncio.ensure_future(foldermap.destroy())
        foldermap = tk.AsyncFrame(manager)
        foldermap.grid(row=1,column=0)
        populate_folder(dir)

    dirbox.bind('<Return>', boxcallback)
    await root.wait_window(manager)
    return manager.dir


async def save():
    print(await file_select())


root.protocol("WM_DELETE_WINDOW", lambda: asyncio.ensure_future(save()))


root.menu = tk.AsyncMenu(root)
root.config(menu=root.menu)


root.dropdown = tk.AsyncMenu(root.menu)

root.dropdown.add_command(label="Do nothing", command=lambda: None)
root.dropdown.add_command(
    label="Save processor time", command=lambda: asyncio.ensure_future(root.destroy())
)

root.menu.add_cascade(label="Unhelpful menu", menu=root.dropdown)


root.mainloop()

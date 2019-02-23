import asynctk as tk
import asyncio
import os
import pathlib

root = tk.AsyncTk()


async def file_select():
    """File select dialogue"""
    manager = tk.AsyncToplevel(root)
    dir = pathlib.Path()
    dirbox = tk.AsyncEntry(manager)
    dirbox.grid(row=0, column=0)
    foldermap = tk.AsyncFrame(manager)
    foldermap.grid(row=1, column=0)

    def populate_folder(folder):
        nonlocal dir
        dir = manager.dir
        for i in ['..'] + os.listdir(folder):
            if (dir / i).is_file():

                async def cb(i=i):
                    manager.file = dir / i
                    await manager.destroy()

                tk.AsyncButton(
                    foldermap,
                    text=f"{i} [FILE]",
                    callback=cb
                ).pack()
            elif (dir / i).is_dir():

                async def cb(i=i):
                    manager.dir = dir / i
                    change_dir(manager.dir)

                tk.AsyncButton(
                    foldermap,
                    text=f"{i} [FOLDER]",
                    callback=cb
                ).pack()
        async def new():
            dialogue = tk.AsyncToplevel(manager)
            filename = tk.AsyncEntry(dialogue)
            filename.pack()
            async def cb():
                if filename.get() != len(filename.get())*'.':
                    for i in r'\/:*?"<>|':
                        if i in filename.get():
                            button.config(text='Save here\n[filename cannot contain any of:\\/:*?"<>|]')
                            break
                    else:
                        manager.file = manager.dir / filename.get()
                        await dialogue.destroy()
                        await manager.destroy()
                else:
                    button.config(text='Save here\n[filename cannot be empty or a special path]')
            button = tk.AsyncButton(dialogue, text='Save here', callback=cb)
            button.pack()
            await manager.wait_window(dialogue)
        tk.AsyncButton(foldermap, text='New file',callback=new).pack()

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
    await root.wait_window(manager)
    return manager.file


async def save():
    print(await file_select())


root.protocol("WM_DELETE_WINDOW", lambda: asyncio.ensure_future(save()))


root.menu = tk.AsyncMenu(root)
root.config(menu=root.menu)


root.dropdown = tk.AsyncMenu(root.menu)

root.dropdown.add_command(label="Do nothing", command=lambda: None)
root.dropdown.add_command(
    label="Save processor time",
    command=lambda: asyncio.ensure_future(root.destroy())
)

root.menu.add_cascade(label="Unhelpful menu", menu=root.dropdown)


root.mainloop()

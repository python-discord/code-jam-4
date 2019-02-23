import asynctk as tk
import asyncio

root = tk.AsyncTk()
async def save():
    print('test')
root.protocol("WM_DELETE_WINDOW", lambda: asyncio.ensure_future(save()))
root.mainloop()
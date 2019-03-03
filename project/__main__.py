from .UI.application import Application
from tkinter import messagebox as mb


def protocal():
    mb.askyesno(None, "Are you sure you want to quit?")
    return protocal()


if __name__ == "__main__":
    app = Application()
    app.bind("<Button-1>", lambda event: mb.showinfo(
        "UPDATE!",
        "we have updated our privacy policy"))
    app.protocol("WM_DELETE_WINDOW", protocal)
    app.mainloop()

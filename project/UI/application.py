import tkinter as tk

class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        self.pages = {}

        self.create_pages()

    def create_pages(self):
        self.pages[HomePage] = HomePage(self)

        self.change_page(HomePage)

    def change_page(self, new_page):
        for page in self.grid_slaves():
            page.grid_remove()

        self.pages[new_page].grid(column=0, row=0)

class HomePage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.create_widgets()

    def create_widgets(self):
        self.title = tk.Label(self, text="Hello World")
        self.title.pack()

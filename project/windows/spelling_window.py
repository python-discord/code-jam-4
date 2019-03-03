import tkinter as tk

class SpellingWindow(tk.Toplevel):
    def __init__(self, master, word):
        super().__init__(master)
        self.word = word

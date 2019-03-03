import tkinter as tk
import json

from .view import Window, View
from . import widget, DOCS, IMAGES


class Question(widget.PrimaryFrame):

    def init(self):
        self.title = widget.PrimaryLabel(self)
        self.choices = widget.SecondaryFrame(self)

        self.options = []

    def load(self, choices):
        for question in questions:
            frame = widget.SecondaryFrame(self.choices)
            check = widget.PrimaryCheckbutton(frame)
            val = widget.SecondaryLabel(frame, text=question)

            frame.pack()
            check.pack(side='left')
            val.pack(side='left')

        self.title.pack(fill='both', expand=True)
        self.choices.pack(fill='both', expand=True)


class Splash(widget.PrimaryFrame):

    intro = (DOCS / 'intro.txt').read_text()  # .replace('\n', ' ').split('  ')
    with (DOCS / 'questions.json').open() as fp:
        questions = json.load(fp)

    def init(self):
        self.window = Window(self)
        self.window.pack(expand=True, fill='both')

        self.intro = View(
            self.window,
            text=self.intro,
            width=self.window.winfo_reqwidth(),
            font=('sys', 14),
            fill='white'
        )
        self.window.set_view(self.intro)

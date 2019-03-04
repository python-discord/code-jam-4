import json

from .view import Window, View
from .animate import Direction, BounceBall
from . import widget, DOCS


class Splash(widget.PrimaryFrame):

    with (DOCS / 'questions.json').open() as fp:
        questions = json.load(fp)

    def init(self):
        self.intro = Intro(self, bg='gray')

        self.btn_confirm = widget.PrimaryButton(
            self.intro.window, command=self.switch, text='Okay'
        )
        self.update()

    def build(self):
        self.update()
        self.intro.pack(fill='both', expand=True)
        self.intro.build()
        self.bounce(
            View(self.intro.window, window=self.btn_confirm)
        )

    def bounce(self, view):
        self.update()
        start = view.master.center + (Direction.LEFT * 175) + (Direction.DOWN * 100)
        wid = view.master.set_view(view, start)
        motion = BounceBall(view.master, wid, view.master.origin, speed=6)
        motion.kick(Direction.UP)
        self.after(0, view.master.run, motion)

    def switch(self):
        self.master.master.switch()

    def cleanup(self):
        self.intro.cleanup()


class Intro(widget.PrimaryFrame):
    intro = (DOCS / 'intro.txt').read_text()

    def init(self):
        self.window = Window(self)
        self.window.pack(expand=True, fill='both')
        self.update()

        width = self.winfo_reqwidth()
        self.title = View(
            self.window,
            text=self.master.master.title(),  # yikes
            font=('Courier', 17),
            width=width, justify='center'
        )
        self.intro = View(
            self.window,
            text=self.intro,
            width=width,
            font=('sys', 12), justify='center'
        )

    def build(self):
        self.update()
        adjust = (Direction.LEFT * 175) + (Direction.DOWN * 100)

        self.window.set_view(self.title)
        self.window.set_view(self.intro, self.window.center + adjust)
        self.update()

    def cleanup(self):
        self.window.animater.clear()


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

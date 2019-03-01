import tkinter as tk
import traceback
from project.windows.cloppy_window_events import CloppyChoiceMadeEvent
from project.functionality.constants import Constants


class CloppyWindow(tk.Toplevel):

    cloppy_image = None

    def __init__(self, master):
        super().__init__(master)

        self.withdraw()

        tk.Grid.rowconfigure(self, index=0, weight=1)
        tk.Grid.columnconfigure(self, index=0, weight=1)

        self.message = None
        self.selected_choice = None

        self.choice_made = CloppyChoiceMadeEvent()

        self.overrideredirect(True)
        self.resizable(False, False)

        if not CloppyWindow.cloppy_image:
            CloppyWindow.cloppy_image = tk.PhotoImage(
                file=Constants.cloppy_picture_path
            )

        self.cloppy_label = tk.Label(self, image=self.cloppy_image)
        self.message_label = tk.Label(self)
        self.input_frame = tk.Frame(self)

        self.cloppy_label.grid(row=0, column=0, sticky=tk.NSEW)
        self.message_label.grid(row=1, column=0, sticky=tk.NSEW)
        self.input_frame.grid(row=2, column=0, sticky=tk.NSEW)

        tk.Grid.columnconfigure(self.input_frame, index=0, weight=1)

        self.grab_set()

    def set_message(self, message):
        self.message = message
        self.message_label.config(text=message)

    def make_choice(self, choice):
        if not self.selected_choice:
            self.selected_choice = choice
            try:
                self.choice_made(self.message, choice)
            except Exception:
                traceback.print_exc()
            finally:
                self.destroy()

    def show(self):
        self.grab_set()
        self.focus_set()
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (self.winfo_width() // 2)
        y = (self.winfo_screenheight() // 2) - (self.winfo_height() // 2)
        self.geometry(f'+{x}+{y}')
        self.deiconify()


class CloppyButtonWindow(CloppyWindow):
    def __init__(self, master):
        super().__init__(master)
        self.choices = {}

    def add_choice(self, choice):
        choice_button = tk.Button(
            self.input_frame,
            text=choice,
            command=lambda: self.make_choice(choice)
        )

        choice_button.grid(row=len(self.choices), column=0, sticky=tk.NSEW)
        tk.Grid.rowconfigure(self, index=len(self.choices), weight=1)

        self.choices[choice] = choice_button


class CloppyInputWindow(CloppyWindow):
    def __init__(self, master):
        super().__init__(master)

        self.input_box = tk.Entry(self.input_frame)
        self.submit_button = tk.Button(
            self.input_frame,
            text='Ok',
            command=lambda: self.make_choice(self.input_box.get())
        )

        self.input_box.grid(row=0, column=0, sticky=tk.NSEW)
        self.submit_button.grid(row=1, column=0, sticky=tk.NSEW)
        self.input_box.bind(
            '<Return>',
            lambda e: self.make_choice(self.input_box.get())
        )

    def show(self):
        super().show()
        self.input_box.focus_set()

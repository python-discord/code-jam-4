import tkinter as tk
import traceback
from typing import List
from project.windows.cloppy_window_events import CloppyChoiceMadeEvent
from project.functionality.constants import Constants


class CloppyWindow(tk.Toplevel):
    """
    This class represents individual 'Cloppy' dialogs. Cloppy is the um...
    'spiritual' equine successor to the infamous MS Word personal assistant
    Clippy. And a fine one at that. Neigh sayers be damned.

    By default, CloppyWindow provides no options to get input from the
    user. That's left up to subclasses to add themselves, by virtue of the
    make_choice method.
    """

    # A reference to the picture used to represent Cloppy.
    # Will be initialized upon first use.
    cloppy_image = None

    def __init__(self, master):
        super().__init__(master)

        # Hide window at first, before it's constructed.
        self.withdraw()

        # Make the window uncloseable, unresizable and unmovable.
        self.overrideredirect(True)
        self.resizable(False, False)

        # Configure grid properties so the elements inside stretch out.
        tk.Grid.rowconfigure(self, index=0, weight=1)
        tk.Grid.rowconfigure(self, index=1, weight=1)
        tk.Grid.rowconfigure(self, index=2, weight=1)
        tk.Grid.rowconfigure(self, index=3, weight=1)
        tk.Grid.columnconfigure(self, index=0, weight=1)

        # The message to be displayed to the user.
        self.message = None

        # The choice selected by the user.
        self.selected_choice = None

        # An event that is fired when the user makes a choice. Call
        # choice_made.add_callback to register callbacks for this event.
        #
        # It sends information to callbacks using a CloppyChoiceMadeEventData
        # object, which contains information about the message displayed to
        # the user and the choice they made in response to it.
        #
        # Check cloppy_window_events.py for the definitions of these classes.
        self.choice_made = CloppyChoiceMadeEvent()

        # Setting up the label containing the image of Cloppy, along with the
        # image data used for this purpose.
        if not CloppyWindow.cloppy_image:
            CloppyWindow.cloppy_image = tk.PhotoImage(
                file=Constants.cloppy_picture_path
            )

        self.cloppy_label = tk.Label(self, image=self.cloppy_image)
        self.cloppy_label.grid(row=0, column=0, sticky=tk.NSEW)

        # Setting up the label containing the greeting to be shown to the user.
        self.greeting_label = tk.Label(self, text=Constants.cloppy_greeting)
        self.greeting_label.grid(row=1, column=0, sticky=tk.NSEW)

        # Setting up the label containing the message to be shown to the user.
        self.message_label = tk.Label(self)
        self.message_label.grid(row=2, column=0, sticky=tk.NSEW)

        # Setting up a frame which will contain the input gathering widgets
        # for this dialog.
        self.input_frame = tk.Frame(self)
        self.input_frame.grid(row=3, column=0, sticky=tk.NSEW)
        tk.Grid.columnconfigure(self.input_frame, index=0, weight=1)

    def set_message(self, message: str):
        """
        Set the message to be displayed to the user in this dialog.

        :param message: The message to display to the user.
        """
        self.message = message
        self.message_label.config(text=message)

    def make_choice(self, choice):
        """
        Called in order to register that a choice has been made in this dialog.
        It will prevent a second choice from being made, as well as fire the
        choice_made event and close the window afterwards.

        :param choice: The choice made from this dialog.
        """
        if not self.selected_choice:
            self.selected_choice = choice

            try:
                self.choice_made(self.message, choice)

            except Exception:
                traceback.print_exc()

            finally:
                self.destroy()

    def show(self):
        """
        Shows the dialog in the middle of the editor window's text box.
        All input and focus is redirected to the dialog while it is open.
        """
        self.grab_set()
        self.focus_set()

        self.update_idletasks()
        self.master.update_idletasks()

        x = (
            self.master.text_box.winfo_rootx() +
            (self.master.text_box.winfo_width()-self.winfo_width()) // 2
        )

        y = (
            self.master.text_box.winfo_rooty() +
            (self.master.text_box.winfo_height()-self.winfo_height()) // 2
        )

        self.geometry(f'+{x}+{y}')
        self.deiconify()


class CloppyButtonWindow(CloppyWindow):
    def __init__(self, master):
        super().__init__(master)

        # A list containing the buttons representing individual choices in the
        # dialog.
        self.choice_buttons: List[tk.Button] = []
        self.highlighted_choice = 0

        # Setting up arrow key event bindings.
        self.bind('<Up>', self.on_up_key)
        self.bind('<Down>', self.on_down_key)

        # Setting up enter key event binding.
        self.bind('<Return>', self.on_enter_key)

    def add_choice(self, choice):
        """
        Add a new button associated with a  choice to the window.

        :param choice: The choice the button represents.
        """
        choice_button = tk.Button(
            self.input_frame,
            text=choice,
            command=lambda: self.make_choice(choice)
        )

        # choice_button.bind('<Up>', self.on_up_key)

        row = len(self.choice_buttons)

        choice_button.grid(
            row=row, column=0, sticky=tk.NSEW
        )

        tk.Grid.rowconfigure(self, index=row, weight=1)

        self.choice_buttons.append(choice_button)

    def show(self):
        super().show()

        if len(self.choice_buttons):
            self.choice_buttons[0].focus_set()

    def set_highlighted_choice(self, choice):
        if choice < 0:
            choice = len(self.choice_buttons)-1
        elif choice >= len(self.choice_buttons):
            choice = 0

        self.highlighted_choice = choice
        self.choice_buttons[choice].focus_set()

    def on_up_key(self, event: tk.Event):
        self.set_highlighted_choice(self.highlighted_choice-1)

    def on_down_key(self, event: tk.Event):
        self.set_highlighted_choice(self.highlighted_choice+1)

    def on_enter_key(self, event: tk.Event):
        self.choice_buttons[self.highlighted_choice].invoke()


class CloppyTextInputWindow(CloppyWindow):
    def __init__(self, master, password=False, submit_button_text='Ok'):
        super().__init__(master)

        if password:
            self.input_box = tk.Entry(self.input_frame, show='*')
        else:
            self.input_box = tk.Entry(self.input_frame)

        self.submit_button = tk.Button(
            self.input_frame,
            text=submit_button_text,
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

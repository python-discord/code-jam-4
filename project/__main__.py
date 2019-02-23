import tkinter as tk
import tkinter.font as tkFont
import math
import json
from pathlib import Path

class UserInterface(tk.Frame):
    def __init__(self, master):
        super().__init__()
        self.text_entry_section = TextEntrySection(self)
        self.keyboard_section = KeyboardSection(self)
        self.text_entry_section.pack()
        self.keyboard_section.pack(ipadx = 5, ipady = 5)

    def receive_key(self, char):
        # Debug, can remove
        print("Recieved {}".format(char))

        self.text_entry_section.receive_key(char)

class TextEntrySection(tk.PanedWindow):
    '''
    This class should contain the text entry box (multiple lines),
        save/load buttons (as well as ctrl-s functionality and such),
        and should look like a generic (albeit extremely barebones)
        text editor.
    It can accept true keyboard input for now, but should also
        accept input from a receive_key method, which is how input
        will be recieved in the future.
    '''
    def __init__(self, master: UserInterface):
        super().__init__()
        self.textbox = tk.Entry(self)
        self.textbox.pack()

    def receive_key(self, char):
        pass #TODO

class KeyboardSection(tk.PanedWindow):
    '''
    This class should contain the dynamically shaped onscreen keyboard,
        which should allow each key to send a receive_key command to
        its master.
    '''
    def __init__(self, master: UserInterface):
        super().__init__()
        self.master = master

        self.buttons = []

        self.grid = tk.Grid()

        self.make_keys()

    def make_keys(self):
        letters = [
            "q",
            "w",
            "e",
            "r",
            "t",
            "y",
            "u",
            "i",
            "o",
            "p",
            "a",
            "s",
            "d",
            "f",
            "g",
            "h",
            "j",
            "k",
            "l",
            "z",
            "x",
            "c",
            "v",
            "b",
            "n",
            "m",
        ]

        self.buttons.append(KeyboardKey(self, "shift"))
        #self.buttons.append(KeyboardKey(self, "a"))

        for letter in letters:
            self.buttons.append(KeyboardKey(self, letter))

        for button in self.buttons:
            button.pack(side = tk.LEFT, ipadx = 5, ipady = 5)

    def send_key(self, char):
        self.master.receive_key(char)

    def toggle_shift(self):
        for button in self.buttons:
            button.toggle_shift()

    def recalc_key_sizes(self, key):
        for button in self.buttons:
            if button is not key:
                button.decrease_scale()
            else:
                button.increase_scale()


class KeyboardKey(tk.Button):
    """
    Represents a key on the keyboard.  Stores relevant data for the key such
    as scale factor, displayed name and actual character value,
    and has methods that change the key in response to different
    user interactions.
    """
    KEY_SIZE = 32

    def __init__(self, master: KeyboardSection, name, char = None, shift_name = None, shift_char = None):
        super().__init__()
        self.master = master

        self.font = tkFont.Font(family="Helvetica", size=KeyboardKey.KEY_SIZE)

        # Letter displayed on the key
        self.name = tk.StringVar()
        self.name.set(name)
        self.text_name = name
        # Letter displayed on the key when shift is active
        self.shift_name = name.upper() if shift_name == None else shift_name
        # Char sent to master when clicked
        if char == None:
            self.char = name.lower()
        else:
            self.char = char
        # Char sent to master when shift is on
        if shift_char == None:
            self.shift_char = self.char.upper()
        else:
            self.shift_char = shift_char
        # Scale factor
        self.scale     = 1.0
        self.scale_inc = 0.1
        self.scale_dec = 0.01
        self.scale_min = 0.5
        self.scale_max = 2.0

        self.clicks    = 0
        self.shift_on  = False

        print("name: {}, char: {}, shift_name: {}, shift_char: {}".format(
            self.text_name,
            self.char,
            self.shift_name,
            self.shift_char,
            )
        )

        if name == "shift":
            button_action = self.send_shift
        else:
            button_action = self.send_key

        self.config (
                textvar    = self.name,
                command = button_action,
                font    = self.font,
                )

    def get_font_size(self):
        return math.floor(KeyboardKey.KEY_SIZE * self.scale)

    def increase_scale(self):
        if self.scale < self.scale_max:
            self.scale += self.scale_inc
        self.font.configure(size=self.get_font_size())

    def decrease_scale(self):
        if self.scale > self.scale_min:
            self.scale -= self.scale_dec
        self.font.configure(size=self.get_font_size())

    def toggle_shift(self):
        self.shift_on = not self.shift_on
        self.name.set(self.text_name if not self.shift_on else self.shift_name)

    def send_key(self):
        self.master.send_key(self.char if not self.shift_on else self.shift_char)

        self.master.recalc_key_sizes(self)

    def send_shift(self):
        self.master.toggle_shift()

        self.master.recalc_key_sizes(self)

if __name__ == '__main__':
    ROOT = tk.Tk()
    UI = UserInterface(ROOT)
    UI.pack()
    ROOT.mainloop()

import tkinter as tk
import tkinter.font as tkFont
import math
import json
# from pathlib import Path


class UserInterface(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        self.text_entry_section = TextEntrySection(self)
        self.keyboard_section = KeyboardSection(self)
        self.text_entry_section.grid(row=0, column=0)
        self.keyboard_section.grid(row=1, column=0, ipadx=5,
                                   ipady=5, sticky="nwse"
                                   )
        self.config(padx=12, pady=12)

    def receive_key(self, char):
        self.text_entry_section.receive_key(char)

    def backspace(self):
        print("Backspace")
        self.text_entry_section.backspace()


class TextEntrySection(tk.Frame):
    '''
    This class should contain the text entry box (multiple lines),
        save/load buttons (as well as ctrl-s functionality and such),
        and should look like a generic (albeit extremely barebones)
        text editor.
    It can accept true keyboard input for now, but should also
        accept input from a receive_key method, which is how input
        will be recieved in the future.
    '''
    def __init__(self, master: UserInterface, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        self.textbox = tk.Text(self, wrap="word", state="disabled")
        self.textbox.grid(row=0, column=0)

    def receive_key(self, char):
        self.textbox.configure(state="normal")
        self.textbox.insert('end', char)
        self.textbox.configure(state="disabled")

    def backspace(self):
        self.textbox.configure(state="normal")
        self.textbox.delete('end - 2 chars', 'end')
        self.textbox.configure(state="disabled")


class KeyboardSection(tk.Frame):
    '''
    This class should contain the dynamically shaped onscreen keyboard,
        which should allow each key to send a receive_key command to
        its master.
    '''
    def __init__(self, master: UserInterface, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        self.master = master

        self.buttons = []

        self.make_keys()

    def make_keys(self):
        with open('keyboard_keys.json') as keyboard_keys_file:
            keyboard = json.load(keyboard_keys_file)

        double_keys = [
            "shift",
            "enter",
            "tab",
            "backspace",
        ]

        for idy, row in enumerate(keyboard):
            for idx, letter in enumerate(row):
                if letter == "":
                    continue
                if isinstance(letter, list):
                    if len(letter) > 2:
                        button = KeyboardKey(self, letter[0],
                                             char=letter[1],
                                             shift_char=letter[2]
                                             )
                    else:
                        button = KeyboardKey(self, letter[0],
                                             shift_char=letter[1]
                                             )
                    letter = letter[0]
                else:
                    button = KeyboardKey(self, letter)
                self.buttons.append(button)
                if letter in double_keys:
                    colspan = 2
                elif letter == "space":
                    colspan = 14
                else:
                    colspan = 1

                button.grid(row=idy, column=idx,
                            columnspan=colspan,
                            sticky="we"
                            )

    def send_key(self, char):
        self.master.receive_key(char)

    def send_backspace(self):
        self.master.backspace()

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

    def __init__(self, master: KeyboardSection, name,
                 char=None, shift_name=None, shift_char=None, *args, **kwargs
                 ):
        tk.Button.__init__(self, master, *args, **kwargs)
        self.master = master

        self.font = tkFont.Font(family="Helvetica", size=KeyboardKey.KEY_SIZE)

        # Letter displayed on the key
        self.name = tk.StringVar()
        self.name.set(name)
        self.text_name = name
        # Letter displayed on the key when shift is active
        if shift_name is None:
            self.shift_name = name.upper() if name.isalpha() else shift_char
        else:
            self.shift_name = shift_name
        # Char sent to master when clicked
        if char is None:
            self.char = name.lower()
        else:
            self.char = char
        # Char sent to master when shift is on
        if shift_char is None:
            self.shift_char = self.char.upper()
        else:
            self.shift_char = shift_char
        # Scale factor
        self.scale = 1.0
        self.scale_inc = 0.1
        self.scale_dec = 0.01
        self.scale_min = 0.5
        self.scale_max = 2.0

        self.clicks = 0
        self.shift_on = False

        # print("name: {}, char: {}, shift_name: {}, shift_char: {}".format(
        #     self.text_name,
        #     self.char,
        #     self.shift_name,
        #     self.shift_char,
        #     )
        # )

        if name == "shift":
            button_action = self.send_shift
        elif name == "backspace":
            button_action = self.send_backspace
        else:
            button_action = self.send_key

        self.config(
            textvar=self.name,
            command=button_action,
            font=self.font,
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
        self.master.send_key(
            self.char if not self.shift_on else self.shift_char
            )

        self.master.recalc_key_sizes(self)

    def send_shift(self):
        self.master.toggle_shift()

        self.master.recalc_key_sizes(self)

    def send_backspace(self):
        self.master.send_backspace()

        self.master.recalc_key_sizes(self)


if __name__ == '__main__':
    ROOT = tk.Tk()
    UI = UserInterface(ROOT)
    UI.pack()
    ROOT.mainloop()

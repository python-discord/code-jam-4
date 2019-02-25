import tkinter as tk
import tkinter.font as tkFont
import math
import json
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent

KEY_DESCRIPTION_PATH = SCRIPT_DIR / Path("key_descriptions.json")
SAVED_KEYS_PATH = SCRIPT_DIR / Path("saved_keyboard.json")
DEFAULT_KEYS_PATH = SCRIPT_DIR / Path("default_keyboard.json")


class UserInterface(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        self.text_entry_section = TextEntrySection(self)
        self.keyboard_section = KeyboardSection(self)
        self.text_entry_section.grid(row=0, column=0)
        self.keyboard_section.grid(row=1, column=0, ipadx=5,
                                   ipady=5, sticky="nwse"
                                   )
        self.config(padx=40, pady=32)

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

        self.keys_per_row = kwargs.pop('keys_per_row', 15)

        self.buttons = []

        try:
            with open(KEY_DESCRIPTION_PATH, 'r') as descriptions_file:
                self.key_descriptions = json.load(descriptions_file)
        except IOError:
            print("Failed to load key_descriptions.json")

        self.make_keys()

    def add_key(self, key_name: str, scale=1.0):
        row_index, col_index = divmod(len(self.buttons), self.keys_per_row)
        key_dict = self.key_descriptions[key_name]
        key_size = key_dict['size']
        new_key = KeyboardKey.from_master_and_dict(self, key_dict)
        new_key.set_scale(scale)
        self.buttons.append(new_key)
        new_key.grid(row=row_index,
                     column=col_index,
                     columnspan=key_size,
                     sticky='we'
                     )

    def make_keys(self):
        try:
            with open(SAVED_KEYS_PATH) as saved_keys_file:
                saved_data = json.load(saved_keys_file)
        except IOError:
            print("Failed to load saved_keyboard.json, loading defaults.")
            try:
                with open(DEFAULT_KEYS_PATH) as saved_keys_file:
                    saved_data = json.load(saved_keys_file)
            except IOError:
                print("Warning: Failed to load default keys.")

        saved_keys = saved_data["keys"]
        saved_scales = saved_data["scales"]

        for idx, key_to_add in enumerate(saved_keys):
            self.add_key(key_to_add, scale=saved_scales[idx])

    def save_keys(self, filepath=SAVED_KEYS_PATH):
        json_compatible_data = {
            'keys': [button.text_name for button in self.buttons],
            'scales': [button.scale for button in self.buttons],
        }
        json_data = json.dumps(json_compatible_data, indent=1)
        try:
            filepath.write_text(json_data)
            return True
        except IOError:
            print("Warning: Failed to save keyboard to file.")
            return False


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

    @classmethod
    def from_master_and_dict(self, master, key_dict):
        return KeyboardKey(master, **key_dict)

    def __init__(self, master: KeyboardSection, name,
                 char=None, shift_name=None, shift_char=None, size=None,
                 *args, **kwargs
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
        self.update_scale()

    def decrease_scale(self):
        if self.scale > self.scale_min:
            self.scale -= self.scale_dec
        self.update_scale()

    def update_scale(self):
        self.font.configure(size=self.get_font_size())

    def set_scale(self, value: float):
        self.scale = value
        self.update_scale()

    def toggle_shift(self):
        self.shift_on = not self.shift_on
        self.name.set(self.text_name if not self.shift_on else self.shift_name)

    def send_key(self):
        self.master.send_key(
            self.char if not self.shift_on else self.shift_char
            )

        if self.scale < self.scale_max:
            self.master.recalc_key_sizes(self)

    def send_shift(self):
        self.master.toggle_shift()

        self.master.recalc_key_sizes(self)

    def send_backspace(self):
        self.master.send_backspace()

        if self.scale < self.scale_max:
            self.master.recalc_key_sizes(self)


def exit_program():
    """
    Save the keyboard before the user closes the window.
    """
    result = UI.keyboard_section.save_keys()
    print("Exiting program, save result: {}".format(result))
    # End the application
    ROOT.destroy()

if __name__ == '__main__':
    ROOT = tk.Tk()
    UI = UserInterface(ROOT)
    UI.pack()
    ROOT.protocol("WM_DELETE_WINDOW", exit_program)
    ROOT.mainloop()

import tkinter as tk
import tkinter.font as tkFont
from tkinter import messagebox
import math
import json
import enchant
import random
from pathlib import Path
# This will be used for images
# from PIL import Image, ImageTk

SCRIPT_DIR = Path(__file__).parent

KEY_DESCRIPTION_PATH = SCRIPT_DIR / Path("key_descriptions.json")
SAVE_DATA_PATH = SCRIPT_DIR / Path("save_data.json")
DEFAULT_KEYS_PATH = SCRIPT_DIR / Path("default_keyboard.json")

ENGLISH_DICTIONARY = enchant.Dict('en_US')

LOOTBOX_RARITIES = {
    0: "common",
    1: "uncommon",
    2: "rare",
    3: "super rare",
    4: "ultra rare",
    5: "legendary"
}

LOOTBOX_RATES = [
    0,
    50,
    70,
    85,
    90,
    95,
]

LOOTBOX_PULLS_PER_BOX = 5


def get_last_word(text):
    # This method is ugly, clean it up later
    assert text.lower() == text
    assert text.strip() == text
    last_known_letter_countback = 1
    try:
        while not text[-last_known_letter_countback].isalpha():
            last_known_letter_countback += 1
    except IndexError:
        return None
    text = text[:1-last_known_letter_countback]
    for i in range(1, len(text)+1):
        if not text[-i].isalpha():
            return text[1-i:]
    return text


class UserInterface(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)

        with open(SAVE_DATA_PATH) as save_data_file:
            save_data = json.load(save_data_file)
        saved_keys = save_data['saved_keys']
        saved_scales = save_data['scales']
        self.used_words = set(save_data['used_words'])

        self.text_entry_section = TextEntrySection(self)
        self.keyboard_section = KeyboardSection(self,
                                                saved_keys=saved_keys,
                                                saved_scales=saved_scales)
        self.text_entry_section.grid(row=0, column=0)
        self.keyboard_section.grid(row=1, column=0, ipadx=5,
                                   ipady=5, sticky="nwse"
                                   )

        key_descriptions = self.keyboard_section.key_descriptions
        self.unlockable_keys = [
                               # common
                               [key_descriptions[key]["name"] for key
                                in key_descriptions
                                if key_descriptions[key]["rarity"] == 0
                                ],
                               # uncommon
                               [key_descriptions[key]["name"] for key
                                in key_descriptions
                                if key_descriptions[key]["rarity"] == 1
                                ],
                               # rare
                               [key_descriptions[key]["name"] for key
                                in key_descriptions
                                if key_descriptions[key]["rarity"] == 2
                                ],
                               # super rare
                               [key_descriptions[key]["name"] for key
                                in key_descriptions
                                if key_descriptions[key]["rarity"] == 3
                                ],
                               # ultra rare
                               [key_descriptions[key]["name"] for key
                                in key_descriptions
                                if key_descriptions[key]["rarity"] == 4
                                ],
                               # legendary
                               [key_descriptions[key]["name"] for key
                                in key_descriptions
                                if key_descriptions[key]["rarity"] == 5
                                ],
                               ]

        self.config(padx=40, pady=32)

    def receive_key(self, char):
        self.text_entry_section.receive_key(char)

    def backspace(self):
        print("Backspace")
        self.text_entry_section.backspace()

    def unlock_lootbox(self):
        print("Lootbox added!")

        for i in range(LOOTBOX_PULLS_PER_BOX):
            rand_int = random.randint(0, 100)
            lootbox_rank = -1
            for threshold in LOOTBOX_RATES:
                if rand_int >= threshold:
                    lootbox_rank += 1

            unlocked_key = random.choice(self.unlockable_keys[lootbox_rank])

            self.keyboard_section.add_key(unlocked_key)

            lootbox_rarity = LOOTBOX_RARITIES[lootbox_rank]

            mbox_title = "{} item unlocked!".format(lootbox_rarity.title())
            mbox_text = "You got a \"{}\"!".format(unlocked_key)

            messagebox.showinfo(
                                mbox_title,
                                mbox_text
                                )

            print("rolled {}".format(rand_int), lootbox_rarity, unlocked_key)

    def on_word_complete(self, last_word: str):
        if last_word is None:
            return
        assert last_word.lower() == last_word
        assert last_word.strip() == last_word
        assert last_word.isalpha()
        if(ENGLISH_DICTIONARY.check(last_word)
           and last_word not in self.used_words):
            self.used_words.add(last_word)
            self.unlock_lootbox()


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
        if len(char) != 1 or not char.isalpha():
            recent_text_in_box = self.textbox.get('end - 50 chars', 'end')
            # -50 chars for constant time complexity (for really long files)
            last_word = get_last_word(recent_text_in_box.strip().lower())
            self.master.on_word_complete(last_word)

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
    def __init__(self, master: UserInterface, saved_keys=set(),
                 saved_scales=set(), *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        self.master = master

        self.keys_per_row = kwargs.pop('keys_per_row', 15)

        self.buttons = []
        self.accumulated_blank_space = 0

        try:
            with open(KEY_DESCRIPTION_PATH, 'r') as descriptions_file:
                self.key_descriptions = json.load(descriptions_file)
        except IOError:
            print("Failed to load key_descriptions.json")

        self.make_keys(saved_keys=saved_keys, saved_scales=saved_scales)

    def add_key(self, key_name: str, scale=1.0):
        row_index, col_index = divmod(
                                      len(self.buttons)
                                      + self.accumulated_blank_space,
                                      self.keys_per_row
                                      )
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
        if key_size > 1:
            self.accumulated_blank_space += key_size - 1

    def make_keys(self, saved_keys=None, saved_scales=None):
        for idx, key_to_add in enumerate(saved_keys):
            self.add_key(key_to_add, scale=saved_scales[idx])

    def save_keys(self, filepath=SAVE_DATA_PATH):
        json_compatible_data = {
            'saved_keys': [button.text_name for button in self.buttons],
            'scales': [button.scale for button in self.buttons],
            'used_words': list(self.master.used_words)
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
                 rarity=None,
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

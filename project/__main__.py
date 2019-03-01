import itertools
import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk
import json
import nltk
from nltk.corpus import words
import random
from pathlib import Path
from PIL import Image, ImageTk
from functools import reduce
import pyaudio
import wave

nltk.download('words', quiet=True, raise_on_error=True)

SCRIPT_DIR = Path(__file__).parent

KEY_DESCRIPTION_PATH = SCRIPT_DIR / Path("key_descriptions.json")
SAVE_DATA_PATH = SCRIPT_DIR / Path("save_data.json")
DEFAULT_SAVE_PATH = SCRIPT_DIR / Path("default_save.json")
IMAGE_PATH = SCRIPT_DIR.parent / Path("img/")
AUDIO_PATH = SCRIPT_DIR.parent / Path("audio/")


audio_player = pyaudio.PyAudio()


def play_sound(soundcode='tap'):
    sound_file = open((AUDIO_PATH / '{}.wav'.format(soundcode)), 'rb')
    sound = wave.open(sound_file, 'rb')

    def audio_callback(in_data, frame_count, time_info, status):
        data = sound.readframes(frame_count)
        return (data, pyaudio.paContinue)

    sound_format = audio_player.get_format_from_width(sound.getsampwidth())
    audio_player.open(format=sound_format,
                      channels=sound.getnchannels(),
                      rate=sound.getframerate(),
                      output=True,
                      stream_callback=audio_callback)


def is_word(text):
    assert text.isalpha()
    return text in words.words()


def calculate_xp(word):
    return len(word)


LOOTBOX_RARITIES = [
    "common",
    "uncommon",
    "rare",
    "super rare",
    "ultra rare",
    "legendary",
]

LOOTBOX_RATES = [0, 50, 70, 85, 90, 95]


LOOTBOX_PULLS_PER_BOX = 5


def get_last_word(text):
    text = text.lower().strip()
    for end_index in range(len(text)-1, -1, -1):
        if text[end_index].isalpha():
            for start_index in range(end_index, -1, -1):
                if not text[start_index].isalpha():
                    return text[start_index+1: end_index+1]
            return text[:end_index+1]
    return None


class UserInterface(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)

        try:
            save_data_file = open(SAVE_DATA_PATH)
        except FileNotFoundError:
            save_data_file = open(DEFAULT_SAVE_PATH)
        finally:
            save_data = json.load(save_data_file)
            save_data_file.close()

        saved_keys = save_data['keys']
        saved_scales = save_data['scales']
        self.used_words = set(save_data['used_words'])

        self.xp_milestones = (index*10 for index in itertools.count())
        self.xp = save_data['xp']
        self.prev_xp_milestone = 0
        self.next_xp_milestone = 0
        while self.xp >= self.next_xp_milestone:
            self.prev_xp_milestone = self.next_xp_milestone
            self.next_xp_milestone = next(self.xp_milestones)

        self.command_section = tk.Frame(self)
        self.text_entry_section = TextEntrySection(self)
        self.keyboard_section = KeyboardSection(self,
                                                saved_keys=saved_keys,
                                                saved_scales=saved_scales)
        self.command_section.grid(row=0, column=0, sticky='nwse')
        self.text_entry_section.grid(row=1, column=0)
        self.keyboard_section.grid(row=2, column=0, ipadx=5,
                                   ipady=5, sticky="nwse"
                                   )

        self.is_darkmode = tk.IntVar()
        tk.Checkbutton(self.command_section, text='Low-Contrast Darkmode',
                       variable=self.is_darkmode,
                       command=self.set_darkmode).pack(side='left')

        self.xp_frame = XPFrame(self.command_section, start_xp=self.xp,
                                prev_xp_milestone=self.prev_xp_milestone,
                                next_xp_milestone=self.next_xp_milestone)
        self.xp_frame.pack(side='right')

        key_descriptions = self.keyboard_section.key_descriptions
        self.unlockable_keys = [[key_descriptions[key]["name"] for key
                                 in key_descriptions
                                 if key_descriptions[key]["rarity"]
                                 == rarity_level]
                                for rarity_level
                                in range(len(LOOTBOX_RARITIES))]

        self.config(padx=40, pady=32)

    def add_xp(self, xp_increase):
        self.xp += xp_increase
        while self.xp >= self.next_xp_milestone:
            self.prev_xp_milestone = self.next_xp_milestone
            self.next_xp_milestone = next(self.xp_milestones)
            self.unlock_lootbox()
        self.xp_frame.set_xp(self.xp,
                             self.prev_xp_milestone,
                             self.next_xp_milestone)

    def set_darkmode(self):
        self.text_entry_section.set_darkmode(self.is_darkmode.get())
        self.keyboard_section.set_darkmode(self.is_darkmode.get())

    def receive_key(self, char):
        play_sound('tap')
        self.text_entry_section.receive_key(char)

    def backspace(self):
        play_sound('tap')
        print("Backspace")
        self.text_entry_section.backspace()

    def unlock_lootbox(self):
        unlocked_keys = []
        rarities = []

        for i in range(LOOTBOX_PULLS_PER_BOX):
            rand_int = random.randint(0, 100)
            lootbox_rank = -1 + len([threshold for threshold in LOOTBOX_RATES
                                     if rand_int >= threshold])
            unlocked_key = random.choice(self.unlockable_keys[lootbox_rank])
            unlocked_keys.append(unlocked_key)
            rarities.append(lootbox_rank)
            self.keyboard_section.add_key(unlocked_key)

        LootBoxUnlockWindow(new_keys=unlocked_keys, rarities=rarities)
        play_sound('pop')

    def on_word_complete(self, last_word: str):
        if last_word is not None:
            assert last_word.lower() == last_word
            assert last_word.strip() == last_word
            assert last_word.isalpha()
            if(is_word(last_word)
               and last_word not in self.used_words):
                self.used_words.add(last_word)
                word_value = calculate_xp(last_word)
                self.add_xp(word_value)


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

    def set_darkmode(self, is_darkmode: bool):
        self.textbox['bg'] = 'black' if is_darkmode else 'white'


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
            'keys': [button.text_name for button in self.buttons],
            'scales': [button.scale for button in self.buttons],
            'used_words': list(self.master.used_words),
            'xp': self.master.xp
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

    def set_darkmode(self, is_darkmode: bool):
        for key in self.buttons:
            key['bg'] = 'black' if is_darkmode else 'SystemButtonFace'


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
        self.char = name.lower() if char is None else char
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

        self.config(textvar=self.name, command=button_action, font=self.font)

    def get_font_size(self):
        return int(KeyboardKey.KEY_SIZE * self.scale)

    def increase_scale(self):
        self.scale = min(self.scale+self.scale_inc, self.scale_max)
        self.update_scale()

    def decrease_scale(self):
        self.scale = max(self.scale-self.scale_dec, self.scale_min)
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
        self.master.send_key(self.shift_char if self.shift_on else self.char)

        if self.scale < self.scale_max:
            self.master.recalc_key_sizes(self)

    def send_shift(self):
        self.master.toggle_shift()

        self.master.recalc_key_sizes(self)

    def send_backspace(self):
        self.master.send_backspace()

        if self.scale < self.scale_max:
            self.master.recalc_key_sizes(self)


class LootBoxUnlockWindow(tk.Toplevel):
    def __init__(self, new_keys=[], rarities=[], *args, **kwargs):
        tk.Toplevel.__init__(self)
        self.iconbitmap(IMAGE_PATH / Path("capsule_small.ico"))
        self.title("Lootbox unlocked!")

        self.attributes("-topmost", True)

        self.new_keys = new_keys
        self.rarities = rarities

        self.lootbox_display = LootBoxUnlockFrame(self)

        tk.Button(self, text="Close", command=self.destroy).pack()

        self.minsize(400, 700)


class LootBoxUnlockFrame(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, master)
        self.master = master

        self.font = tkFont.Font(size=64)

        image_data1 = Image.open(IMAGE_PATH / Path("capsule1.png"))
        image_data2 = Image.open(IMAGE_PATH / Path("capsule2.png"))
        self.img_capsule = [
            ImageTk.PhotoImage(image_data1),
            ImageTk.PhotoImage(image_data2)
        ]

        self.lootbox_text = tk.StringVar()
        self.lootbox_text.set("Lootbox get!")

        self.text_label = tk.Label(self, textvar=self.lootbox_text,
                                   font=self.font
                                   )
        self.text_label.pack()

        self.image_label = tk.Label(self, image=self.img_capsule[0])
        self.image_label.image = self.img_capsule[0]
        self.image_label.pack()

        self.message_label = tk.Label(self, text="", height=10, width=20,
                                      justify=tk.LEFT)
        self.message_label.pack()

        self.pack()

        self.after(1000, self.open_lootbox)

    def open_lootbox(self):
        new_keys = [
            "{} ({})".format(key, LOOTBOX_RARITIES[self.master.rarities[idx]])
            for idx, key in enumerate(self.master.new_keys)
            ]

        new_keys_str = reduce(
            lambda x, y: "{}\n{}".format(x, y), new_keys
            )
        self.image_label.config(image=self.img_capsule[1])
        self.image_label.image = self.img_capsule[1]
        self.message_label['text'] = "You got:\n {}".format(new_keys_str)


class XPFrame(tk.Frame):
    def __init__(self, master, xp=0, prev_xp_milestone=0,
                 next_xp_milestone=0, *args, **kwargs):
        tk.Frame.__init__(self, master)
        self.prev_xp_label = tk.Label(self, text=prev_xp_milestone)
        self.xp_label = tk.Label(self, text="XP:{}".format(xp),
                                 font=('Helvetica 18 bold'))
        self.next_xp_label = tk.Label(self, text=next_xp_milestone)
        self.xp_progressbar = ttk.Progressbar(self, orient='horizontal',
                                              mode='determinate',
                                              maximum=next_xp_milestone
                                              - prev_xp_milestone,
                                              value=xp-prev_xp_milestone)
        lootbox_image_data = Image.open(IMAGE_PATH / Path("capsule_small.ico"))
        self.lootbox_image = ImageTk.PhotoImage(lootbox_image_data)
        self.lootbox_image_label = tk.Label(self, image=self.lootbox_image)
        self.xp_label.pack(side='left')
        self.prev_xp_label.pack(side='left')
        self.xp_progressbar.pack(side='left')
        self.next_xp_label.pack(side='left')
        self.lootbox_image_label.pack(side='left')

    def set_xp(self, xp, prev_xp_milestone, next_xp_milestone):
        self.xp_label['text'] = "XP:{}".format(xp)
        self.prev_xp_label['text'] = prev_xp_milestone
        self.next_xp_label['text'] = next_xp_milestone
        self.xp_progressbar['maximum'] = next_xp_milestone - prev_xp_milestone
        self.xp_progressbar['value'] = xp - prev_xp_milestone


def exit_program():
    """
    Save the keyboard before the user closes the window.
    """
    save_successful = UI.keyboard_section.save_keys()
    if not save_successful:
        print("Exiting program, failed to save.")
    audio_player.terminate()
    ROOT.destroy()


if __name__ == '__main__':
    ROOT = tk.Tk()
    ROOT.title('User Friendly Text Editor (change name)')
    ROOT.iconbitmap(IMAGE_PATH / "window_icon.ico")
    UI = UserInterface(ROOT)
    UI.pack()
    ROOT.protocol("WM_DELETE_WINDOW", exit_program)
    ROOT.mainloop()

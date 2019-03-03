'''
(The features of this codejam project are not to be taken seriously)
Code Jam 4 submission for High Houses of Adorable Laboratories: HTT
HTT is used to run a text editor with a built-in onscreen keyboard.
Go ahead, give it a try! Our tutorial will walk you through how to use it!
'''
import asyncio
import os
import threading
import itertools
import tkinter as tk
import tkinter.font as tkFont
from tkinter import filedialog as fd
from tkinter import messagebox
from tkinter import ttk
import json
import random
from pathlib import Path
import wave
from PIL import Image, ImageTk
import pyaudio


SCRIPT_DIR = Path(__file__).parent

KEY_DESCRIPTION_PATH = SCRIPT_DIR / Path('key_descriptions.json')
SAVE_DATA_PATH = SCRIPT_DIR / Path('save_data.json')
WORDS_PATH = SCRIPT_DIR / Path('words.json')
DEFAULT_SAVE_PATH = SCRIPT_DIR / Path('default_save.json')
TUTORIALS_PATH = SCRIPT_DIR / Path('tutorials.json')
IMAGE_PATH = SCRIPT_DIR.parent / Path('img/')
AUDIO_PATH = SCRIPT_DIR.parent / Path('audio/')
DEFAULT_DOC_PATH = SCRIPT_DIR.parent / Path('documents/')

IMAGE_PATHS = {'new_icon': IMAGE_PATH / 'new_icon.png',
               'open_icon': IMAGE_PATH / 'open_icon.png',
               'save_icon': IMAGE_PATH / 'save_icon.png',
               'capsule_small': IMAGE_PATH / 'capsule_small.ico',
               'capsule1': IMAGE_PATH / 'capsule1.png',
               'capsule2': IMAGE_PATH / 'capsule2.png',
               'tutorial_smirk': IMAGE_PATH / 'tutorial_smirk.png',
               'tutorial_neutral': IMAGE_PATH / 'tutorial_neutral.png',
               'window_icon': IMAGE_PATH / 'window_icon.ico'
               }


audio_player = pyaudio.PyAudio()

AUDIO_CHUNK_SIZE = 1024


async def mainloop_coro(root):
    '''
    Coroutine that mimics tk.mainloop.
    It should sleep after update such that async tasks can be completed.
    Will run until window is closed.
    '''
    try:
        while True:
            root.update()
            root.update_idletasks()
            await asyncio.sleep(0)
    except tk.TclError:
        return


valid_soundcodes = [filename.replace('.wav', '')
                    for filename in os.listdir(AUDIO_PATH)
                    if filename.endswith('.wav')]


def get_sound_data(soundcode):
    '''
    Returns a tuple of (stream, sound, sound_file) for a given soundcode.
    Soundcode should be the name of a .wav file in AUDIO_PATH without .wav.
    '''

    sound_file = open((AUDIO_PATH / '{}.wav'.format(soundcode)), 'rb')
    sound = wave.open(sound_file, 'rb')
    sound_format = audio_player.get_format_from_width(sound.getsampwidth())
    stream = audio_player.open(format=sound_format,
                               channels=sound.getnchannels(),
                               rate=sound.getframerate(),
                               output=True)
    return stream, sound, sound_file


sound_streams = {soundcode: [get_sound_data(soundcode) for i in range(10)]
                 for soundcode in valid_soundcodes}


def prepare_sound(soundcode):
    '''Add a sound to the prepared sounds (makes play_sound faster)'''
    sound_streams[soundcode].append(get_sound_data(soundcode))


def play_sound(soundcode='tap'):
    '''
    Plays a sound!
    Soundcode must be the name of a .wav file in code_jam_4/audio.
    Soundcode must not include the .wav extension.
    Creates:
    *A thread to play the audio
    *A thread to prepare the next audio stream (to minimize latency)
    '''
    if soundcode not in valid_soundcodes:
        raise ValueError("Soundcode must be one of \
                          {}".format(valid_soundcodes))

    def play_and_close():
        stream, wave_file, path_file = sound_streams[soundcode].pop()
        data = wave_file.readframes(AUDIO_CHUNK_SIZE)
        while data:
            stream.write(data)
            data = wave_file.readframes(AUDIO_CHUNK_SIZE)
        stream.stop_stream()
        for sound_datum_to_close in stream, wave_file, path_file:
            sound_datum_to_close.close()
    threading.Thread(target=play_and_close).start()
    threading.Thread(target=prepare_sound, args=(soundcode,)).start()


with open(WORDS_PATH, 'r') as words_file:
    real_words = set(json.load(words_file))


def is_word(text):
    '''Returns whether the given word is accepted as an English word.'''
    assert text.isalpha()
    return text.lower() in real_words


LETTER_SCORES = {'a': 1, 'e': 1, 'i': 1, 'u': 1, 'n': 1, 'r': 1, 'o': 1,
                 's': 1, 'l': 1, 't': 1, 'd': 2, 'g': 2, 'm': 3, 'b': 3,
                 'c': 3, 'p': 3, 'y': 4, 'f': 4, 'v': 4, 'w': 4, 'h': 4,
                 'k': 5, 'j': 8, 'x': 8, 'q': 10, 'z': 10}


def calculate_xp(word):
    '''
    Returns the XP value of a word.
    This method can be overridden with a different XP algorithm.
    '''
    return sum([LETTER_SCORES[letter] for letter in word])


LOOTBOX_RARITIES = [
    'common',
    'uncommon',
    'rare',
    'super rare',
    'ultra rare',
    'legendary',
]

LOOTBOX_RATES = [0, 50, 70, 85, 90, 95]


LOOTBOX_PULLS_PER_BOX = 5


def get_last_word(text):
    '''
    Given a string, returns the string of letters separated by punctuation \
    closest to the end.
    'Hi;There!how are*you?' -> 'you'
    '''
    text = text.lower().strip()
    for end_index in range(len(text)-1, -1, -1):
        if text[end_index].isalpha():
            for start_index in range(end_index, -1, -1):
                if not text[start_index].isalpha():
                    return text[start_index+1: end_index+1]
            return text[:end_index+1]
    return None


class UserInterface(tk.Frame):
    '''
    Main frame of the HTT program. Should be packed into root.
    Also contains general program functions not directly related to UI.
    '''
    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)

        try:
            save_data_file = open(SAVE_DATA_PATH)
        except FileNotFoundError:
            save_data_file = open(DEFAULT_SAVE_PATH)
        finally:
            save_data = json.load(save_data_file)
            save_data_file.close()

        with open(TUTORIALS_PATH, 'r') as tutorials_file:
            all_tutorials = json.load(tutorials_file)

        self.window_name = 'Typing Program'

        saved_keys = save_data['keys']
        saved_scales = save_data['scales']
        self.tutorials = {trigger: data for trigger, data
                          in all_tutorials.items() if trigger
                          in save_data['tutorials']}
        self.used_words = set(save_data['used_words'])

        if 'working_directory' in save_data.keys():
            self.working_directory = Path(save_data['working_directory'])
        else:
            self.working_directory = DEFAULT_DOC_PATH

        self.working_file = None

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
        self.command_section.pack(side='top', fill='x')
        self.text_entry_section.pack(side='top', fill='x')
        self.keyboard_section.pack(side='top', ipadx=5, ipady=5)

        self.icons = {file_option:
                      ImageTk.PhotoImage(
                          Image.open(IMAGE_PATHS[f'{file_option}_icon']))
                      for file_option in ['new', 'save', 'open']}

        self.new_button = tk.Button(self.command_section,
                                    image=self.icons['new'],
                                    command=self.new_file,
                                    ).pack(side='left')

        self.save_button = tk.Button(self.command_section,
                                     image=self.icons['save'],
                                     command=self.save_file,
                                     ).pack(side='left')

        self.open_button = tk.Button(self.command_section,
                                     image=self.icons['open'],
                                     command=self.load_file,
                                     ).pack(side='left')

        self.is_darkmode = tk.IntVar()
        tk.Checkbutton(self.command_section, text='Low-Contrast Darkmode',
                       variable=self.is_darkmode,
                       command=self.set_darkmode).pack(side='left')

        self.xp_frame = XPFrame(self.command_section, xp=self.xp,
                                prev_xp_milestone=self.prev_xp_milestone,
                                next_xp_milestone=self.next_xp_milestone)
        self.xp_frame.pack(side='right')

        key_descriptions = self.keyboard_section.key_descriptions
        self.unlockable_keys = [[key_descriptions[key]['name'] for key
                                 in key_descriptions
                                 if key_descriptions[key]['rarity']
                                 == rarity_level]
                                for rarity_level
                                in range(len(LOOTBOX_RARITIES))]

        self.config(padx=40, pady=16)

        self.menu = tk.Menu(self.master)
        self.master.config(menu=self.menu)

        file_menu = tk.Menu(self.menu)
        self.menu.add_cascade(label='File', menu=file_menu)

        file_menu.add_command(label='New', command=self.new_file)
        file_menu.add_command(label='Save', command=self.save_file)
        file_menu.add_command(label='Save As', command=self.save_file_as)
        file_menu.add_command(label='Load', command=self.load_file)
        file_menu.add_command(label='Quit', command=exit_program)

        self.tutorial_trigger('start')

    def tutorial_trigger(self, trigger):
        '''
        Called when a tutorial trigger is reached.
        If the user has not yet seen the given tutorial, it will play.
        '''
        if trigger in self.tutorials:
            tutorial_data = self.tutorials.pop(trigger)
            TutorialWindow(self, tutorial_data['text'], tutorial_data['smirk'])

    def new_file(self):
        '''Called when the user requests a new file'''
        self.working_file = None
        self.text_entry_section.set_text('')

    def save_file(self):
        '''
        Called when the user requests their file be saved
        User wishes to overwrite the existing file if possible
        '''
        if self.working_file is None:
            self.save_file_as()
        else:
            self.write_file(self.working_file)

    def save_file_as(self):
        '''
        Called when the user requests their file be saved
        User wishes to (or must) specify file save location
        '''
        filepath = fd.asksaveasfilename(initialdir=self.working_directory,
                                        title='Save as...',
                                        filetypes=(('text files', '.txt'),
                                                   ('all files', '*.*')))
        if filepath:
            self.working_file = filepath
            self.write_file(filepath)

    def write_file(self, filepath):
        '''Writes textentry data to a given filepath'''
        doc_text = self.text_entry_section.get_text()
        try:
            Path(filepath).write_text(doc_text)
        except IOError:
            messagebox.showinfo('Error', 'Error saving file')
        else:
            messagebox.showinfo(self.window_name, 'Save complete.')

    def load_file(self):
        '''Called when the user wishes to load a file'''
        filepath = fd.askopenfilename(initialdir=self.working_directory,
                                      title='Open file',
                                      filetypes=(('text files', '.txt'),
                                                 ('all files', '*.*')))
        if filepath:
            filepath = Path(filepath)
            try:
                doc_text = filepath.read_text()
            except IOError:
                messagebox.showinfo('Error', 'Error loading file')
            else:
                self.text_entry_section.set_text(doc_text)
                self.text_entry_section.backspace()
                self.working_file = str(filepath)

    def add_xp(self, xp_increase):
        '''Adds a given amount of XP to the user's XP value.'''
        self.xp += xp_increase
        while self.xp >= self.next_xp_milestone:
            self.prev_xp_milestone = self.next_xp_milestone
            self.next_xp_milestone = next(self.xp_milestones)
            self.unlock_lootbox()
        self.xp_frame.set_xp(self.xp,
                             self.prev_xp_milestone,
                             self.next_xp_milestone)
        self.tutorial_trigger('xpgain')

    def set_darkmode(self):
        '''
        User has toggled the darkmode setting
        Toggles the background of certain elements on the UI
        '''
        self.text_entry_section.set_darkmode(self.is_darkmode.get())
        self.keyboard_section.set_darkmode(self.is_darkmode.get())
        self.tutorial_trigger('darkmode')

    def receive_key(self, char):
        '''
        Called when the onscreen keyboard has recognized a keystroke.
        Backspace will not call this; it will instead call backspace
        '''
        play_sound('tap')
        self.text_entry_section.receive_key(char)
        self.tutorial_trigger('grow')

    def backspace(self):
        '''Called when the onscreen keyboard has recognized a backspace'''
        play_sound('tap')
        self.text_entry_section.backspace()

    def unlock_lootbox(self):
        '''Adds a lootbox (the keys contained) to the user's keyboard'''
        unlocked_keys = []
        rarities = []

        for _ in range(LOOTBOX_PULLS_PER_BOX):
            rand_int = random.randint(0, 100)
            lootbox_rank = -1 + len([threshold for threshold in LOOTBOX_RATES
                                     if rand_int >= threshold])
            unlocked_key = random.choice(self.unlockable_keys[lootbox_rank])
            unlocked_keys.append(unlocked_key)
            rarities.append(lootbox_rank)
            self.keyboard_section.add_key(unlocked_key)

        LootBoxUnlockWindow(new_keys=unlocked_keys, rarities=rarities)
        self.tutorial_trigger('lootbox')
        play_sound('decision4')

    def on_word_complete(self, last_word: str):
        '''
        Called when the user has completed a word.
        Checks for valid words and their respective XP gain
        '''
        if last_word:
            assert last_word.lower() == last_word
            assert last_word.strip() == last_word
            assert last_word.isalpha()
            if(is_word(last_word)
               and last_word not in self.used_words):
                self.used_words.add(last_word)
                word_value = calculate_xp(last_word)
                self.add_xp(word_value)
            else:
                self.tutorial_trigger('fakeword')


class TextEntrySection(tk.Frame):
    '''
    This class contains the text entry box, and its appropriate methods.
    Accepts input from the onscreen keyboard.
    Blocks input from the true keyboard.
    '''
    def __init__(self, master: UserInterface, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        self.textbox = tk.Text(self, wrap='word', state='disabled')
        self.textbox.pack(fill='x')

    def receive_key(self, char):
        '''
        Called when the onscreen keyboard has recognized a keystroke.
        Backspace will not call this; it will instead call backspace
        '''
        self.textbox.configure(state='normal')
        self.textbox.insert('end', char)
        self.textbox.configure(state='disabled')
        if len(char) != 1 or not char.isalpha():
            recent_text_in_box = self.textbox.get('end - 50 chars', 'end')
            # -50 chars for constant time complexity (for really long files)
            last_word = get_last_word(recent_text_in_box.strip().lower())
            self.master.on_word_complete(last_word)

    def backspace(self):
        '''Removes the last character in the textbox'''
        self.textbox.configure(state='normal')
        self.textbox.delete('end - 2 chars', 'end')
        self.textbox.configure(state='disabled')

    def set_darkmode(self, is_darkmode: bool):
        '''Toggles the darkmode background of the textbox'''
        self.textbox['bg'] = 'black' if is_darkmode else 'white'

    def get_text(self):
        '''Returns the contents of the textbox'''
        return self.textbox.get(1.0, 'end')

    def set_text(self, new_text):
        '''
        Sets the entire text of the textbox.
        Should only be used for new files or loading a file
        '''
        self.textbox.configure(state='normal')
        self.textbox.delete(1.0, 'end')
        self.textbox.insert(1.0, new_text)
        self.textbox.configure(state='disabled')


class KeyboardSection(tk.Frame):
    '''Contains the dynamically shaped onscreen keyboard and its keys'''
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
            print('Failed to load key_descriptions.json')

        for idx, key_to_add in enumerate(saved_keys):
            self.add_key(key_to_add, scale=saved_scales[idx])

    def add_key(self, key_name: str, scale=1.0):
        '''
        Adds a key to the keyboard.
        Generally only called on initialization or lootbox unlock.
        '''
        row_index, col_index = divmod(len(self.buttons)
                                      + self.accumulated_blank_space,
                                      self.keys_per_row)
        key_dict = self.key_descriptions[key_name]
        key_size = key_dict['size']
        new_key = KeyboardKey(self, **key_dict)
        new_key.set_scale(scale)
        self.buttons.append(new_key)
        new_key.grid(row=row_index,
                     column=col_index,
                     columnspan=key_size,
                     sticky='we'
                     )
        if key_size > 1:
            self.accumulated_blank_space += key_size - 1

    def save(self, filepath=SAVE_DATA_PATH):
        '''
        Saves the user's XP/keys/etc progress
        This does NOT save the text file
        '''
        json_compatible_data = {
            'keys': [button.text_name for button in self.buttons],
            'scales': [button.scale for button in self.buttons],
            'used_words': list(self.master.used_words),
            'xp': self.master.xp,
            'tutorials': list(self.master.tutorials.keys()),
            'working_directory': str(self.master.working_directory)
        }
        json_data = json.dumps(json_compatible_data, indent=1)
        try:
            filepath.write_text(json_data)
            return True
        except IOError:
            print('Warning: Failed to save keyboard to file.')
            return False

    def send_key(self, char):
        '''Sends a key to ther UserInterface'''
        self.master.receive_key(char)

    def send_backspace(self):
        '''Sends a backspace to the UserInterface'''
        self.master.backspace()

    def toggle_shift(self):
        '''Toggles the shift value of all keys'''
        for button in self.buttons:
            button.toggle_shift()

    def recalc_key_sizes(self, key):
        '''Rescales all keys, given the grow key'''
        for button in self.buttons:
            if button is not key:
                button.decrease_scale()
            else:
                button.increase_scale()

    def set_darkmode(self, is_darkmode: bool):
        '''Toggles the background of the key'''
        for key in self.buttons:
            key['bg'] = 'black' if is_darkmode else 'SystemButtonFace'


class KeyboardKey(tk.Button):
    '''
    Represents a key on the keyboard.  Stores relevant data for the key such
    as scale factor, displayed name and actual character value,
    and has methods that change the key in response to different
    user interactions.
    '''
    KEY_SIZE = 32

    def __init__(self, master: KeyboardSection, name,
                 char=None, shift_name=None, shift_char=None, size=None,
                 rarity=None, *args, **kwargs):
        tk.Button.__init__(self, master, *args, **kwargs)
        self.master = master

        self.font = tkFont.Font(family='Helvetica', size=KeyboardKey.KEY_SIZE)

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

        if name == 'shift':
            button_action = self.send_shift
        elif name == 'backspace':
            button_action = self.send_backspace
        else:
            button_action = self.send_key

        self.config(textvar=self.name, command=button_action, font=self.font)

    def get_font_size(self):
        '''Returns the font size of the individual key'''
        return int(KeyboardKey.KEY_SIZE * self.scale)

    def increase_scale(self):
        '''Increases the scale of the individual key'''
        self.scale = min(self.scale+self.scale_inc, self.scale_max)
        self.font.configure(size=self.get_font_size())

    def decrease_scale(self):
        '''Decreases the scale of the individual key'''
        self.scale = max(self.scale-self.scale_dec, self.scale_min)
        self.font.configure(size=self.get_font_size())

    def set_scale(self, value: float):
        '''Sets the scale of the individual key'''
        self.scale = value
        self.font.configure(size=self.get_font_size())

    def toggle_shift(self):
        '''
        Toggles shift value for the invididual key.
        (a -> A) or (A -> a)
        '''
        self.shift_on = not self.shift_on
        self.name.set(self.text_name if not self.shift_on else self.shift_name)

    def send_key(self):
        '''Sends the key's value to the master, after being tapped.'''
        self.master.send_key(self.shift_char if self.shift_on else self.char)

        if self.scale < self.scale_max:
            self.master.recalc_key_sizes(self)

    def send_shift(self):
        '''
        Sends a shift signal to master, after shift is tapped.'''
        self.master.toggle_shift()

        self.master.recalc_key_sizes(self)

    def send_backspace(self):
        self.master.send_backspace()

        if self.scale < self.scale_max:
            self.master.recalc_key_sizes(self)


class LootBoxUnlockWindow(tk.Toplevel):
    '''Represents the window conaining the lootbox frame'''
    def __init__(self, new_keys=[], rarities=[], *args, **kwargs):
        tk.Toplevel.__init__(self)
        self.iconbitmap(IMAGE_PATHS['capsule_small'])
        self.title('Lootbox unlocked!')

        self.attributes('-topmost', True)

        self.new_keys = new_keys
        self.rarities = rarities

        self.lootbox_display = LootBoxUnlockFrame(self)

        tk.Button(self, text='Close', command=self.destroy).pack()

        self.minsize(400, 700)


class LootBoxUnlockFrame(tk.Frame):
    '''Frame that contains lootbox unlock information such as keys unlocked'''
    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, master)
        self.master = master

        self.font = tkFont.Font(size=64)

        lootbox_closed_image_data = Image.open(IMAGE_PATHS['capsule1'])
        lootbox_open_image_data = Image.open(IMAGE_PATHS['capsule2'])
        self.img_capsule = [
            ImageTk.PhotoImage(lootbox_closed_image_data),
            ImageTk.PhotoImage(lootbox_open_image_data)]

        self.text_label = tk.Label(self, text='Lootbox get!',
                                   font=self.font)
        self.text_label.pack()

        self.image_label = tk.Label(self, image=self.img_capsule[0])
        self.image_label.pack()

        self.message_label = tk.Label(self, text='', height=10, width=20,
                                      justify=tk.LEFT)
        self.message_label.pack()

        self.pack()

        self.after(1000, self.open_lootbox)

    def open_lootbox(self):
        '''Opens a lootbox and adds the contained keys'''
        play_sound('pop')
        new_keys = [
            '{} ({})'.format(key, LOOTBOX_RARITIES[self.master.rarities[idx]])
            for idx, key in enumerate(self.master.new_keys)
            ]
        self.image_label.config(image=self.img_capsule[1])
        self.message_label['text'] = 'You got:\n{}'.format('\n'.join(new_keys))


class XPFrame(tk.Frame):
    '''Frame that isplays XP information, such as current value and progress'''
    def __init__(self, master, xp=0, prev_xp_milestone=0,
                 next_xp_milestone=0, *args, **kwargs):
        tk.Frame.__init__(self, master)
        self.prev_xp_label = tk.Label(self, text=prev_xp_milestone)
        self.xp_label = tk.Label(self, text='XP:{}'.format(xp),
                                 font=('Helvetica 18 bold'))
        self.next_xp_label = tk.Label(self, text=next_xp_milestone)
        self.xp_progressbar = ttk.Progressbar(self, orient='horizontal',
                                              mode='determinate',
                                              maximum=next_xp_milestone
                                              - prev_xp_milestone,
                                              value=xp-prev_xp_milestone)
        lootbox_image_data = Image.open(IMAGE_PATHS['capsule_small'])
        self.lootbox_image = ImageTk.PhotoImage(lootbox_image_data)
        self.lootbox_image_label = tk.Label(self, image=self.lootbox_image)
        self.xp_label.pack(side='left')
        self.prev_xp_label.pack(side='left')
        self.xp_progressbar.pack(side='left')
        self.next_xp_label.pack(side='left')
        self.lootbox_image_label.pack(side='left')

    def set_xp(self, xp, prev_xp_milestone, next_xp_milestone):
        '''Adjusts the displayed XP vaue'''
        self.xp_label['text'] = 'XP:{}'.format(xp)
        self.prev_xp_label['text'] = prev_xp_milestone
        self.next_xp_label['text'] = next_xp_milestone
        self.xp_progressbar['maximum'] = next_xp_milestone - prev_xp_milestone
        self.xp_progressbar['value'] = xp - prev_xp_milestone


class TutorialWindow(tk.Toplevel):
    '''Window containing a tutorial message'''

    previous_tutorial_window = None

    def __init__(self, master, message=None, smirk=False, *args, **kwargs):
        tk.Toplevel.__init__(self)

        if TutorialWindow.previous_tutorial_window:
            TutorialWindow.previous_tutorial_window.destroy()
        TutorialWindow.previous_tutorial_window = self

        self.master = master
        self.title('Tutorial')
        self.attributes('-topmost', True)

        self.message_label = tk.Text(self,
                                     font=('comic', 12),
                                     width=60,
                                     height=20,
                                     wrap=tk.WORD,
                                     )
        self.message_label.insert(1.0, message)
        self.message_label.config(state='disabled')
        image_path = IMAGE_PATH / Path('tutorial_smirk.png' if smirk else
                                       'tutorial_neutral.png')
        self.tutorial_image = ImageTk.PhotoImage(Image.open(image_path))
        self.image_label = tk.Label(self, image=self.tutorial_image)
        self.message_label.pack(side='left')
        self.image_label.pack(side='right')
        tk.Button(self, text="Close", command=self.destroy).pack(side='bottom')

        self.config(padx=20, pady=20)


def exit_program():
    '''Save the keyboard before the user closes the window.'''
    save_successful = UI.keyboard_section.save()
    if not save_successful:
        print('Exiting program, failed to save.')
    audio_player.terminate()
    ROOT.destroy()


if __name__ == '__main__':
    ROOT = tk.Tk()
    ROOT.title('High Tech Text (HTT) Editor')
    ROOT.iconbitmap(IMAGE_PATHS['window_icon'])
    UI = UserInterface(ROOT)
    UI.pack()
    ROOT.protocol('WM_DELETE_WINDOW', exit_program)
    asyncio.get_event_loop().run_until_complete(mainloop_coro(ROOT))

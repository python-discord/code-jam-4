import tkinter as tk

class UserInterface(tk.Frame):
    def __init__(self, master):
        super().__init__()
        self.text_entry_section = TextEntrySection(self)
        self.keyboard_section = KeyboardSection(self)
        self.text_entry_section.pack()
        self.keyboard_section.pack()

    def receive_key(self, char):
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
        tk.Label(self, text="(Keyboard goes here)").pack()
        '''Remove this; it's for helping TextEntrySelection person ^^^ '''

if __name__ == '__main__':
    ROOT = tk.Tk()
    UI = UserInterface(ROOT)
    UI.pack()
    ROOT.mainloop()

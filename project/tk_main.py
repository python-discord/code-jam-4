import tkinter as tk

KEYBOARD = "lower"
#valid args: "lower", "upper", "special", "numbers", "punctuation"

class alph_aerobics (tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()

        self.characters = {
            'punctuation' : list(map(chr, range(32, 47))),
            'numbers': list(map(chr, range(48, 58))),
            'special': list(map(chr, range(58, 65))),
            'upper': list(map(chr, range(65, 91))),
            'lower': list(map(chr, range(97, 123))),
        }
        
        self.text_box = None
        self.text = "Sample_text"
        
        self.create_window()

    def create_window(self):
        """Creates the main text editor window"""
        
        self.text_box = tk.Text(self)
        self.text_box.grid(columnspan=9)
        
        self.create_keyboard(KEYBOARD)

    def create_keyboard(self, which_keyboard, num_columns = 9):
        """Creates the keyboard specified by which_keyboard.
        num_columns specifies the width of the keyboard
        """
        index = num_columns
        for key in self.characters[which_keyboard]:
            self.create_button(key, int(index % num_columns),
                               int(index / num_columns))
            index += 1

    def create_button(self, char, c, r):
        """Creates a button at (c, r).
        When pressed, the button appends char to the text_box"""
        b = tk.Button(
            self,
            text=str(char),
            command=lambda: self.text_box.insert(tk.CURRENT, str(char)),
            width = 6,
            background ="#23D085",
            )
        b.grid(column = c, row = r)


root = tk.Tk()
app = alph_aerobics(master=root)
app.mainloop()


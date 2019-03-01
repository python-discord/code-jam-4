import tkinter as tk


class alph_aerobics (tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()

        self.characters = {
            'punctuation': list(map(chr, range(32, 47))),
            'numbers': list(map(chr, range(48, 58))),
            'special': list(map(chr, range(58, 65))),
            'upper': list(map(chr, range(65, 91))),
            'lower': list(map(chr, range(97, 123))),
        }

        self.text_box = None
        self.text = "Sample_text"
        self.create_window()
        b = tk.Button(
            self,
            text="For testing features",
            command=lambda: print(self.text_box.config(state="disabled")),
            background="black",
            foreground="white",
            )
        b.grid(row=15, columnspan=3, sticky="w")

    def create_window(self):
        """Creates the main app window"""
        self.text_box = tk.Text(self, state="disabled")
        self.text_box.grid(row=10, columnspan=9)
        self.switch_keyboard("upper")

        # keyboard_select is a list of the keyboard buttons, so that these
        # buttons can be made toggleable.
        keyboard_select = []
        idx = 0
        for keyboard in self.characters.keys():
            b = self.create_keyboard_button(16, idx, keyboard)
            keyboard_select.append(b)
            idx += 1

    def switch_keyboard(self, which_keyboard, num_columns=9):
        """Replaces current keyboard with which_keyboard.
        num_columns specifies the width of the keyboard - defaults to 9.
        """
        for r in range(20, 24):
            keys = self.grid_slaves(row=r)
            for key in keys:
                key.destroy()
        
        index = 20 * num_columns
        for key in self.characters[which_keyboard]:
            self.create_key(key, int(index % num_columns),
                            int(index / num_columns))
            index += 1

    def create_key(self, char, c, r):
        """Helper method that creates a button at (c, r).
        When pressed, the button appends char to the text_box"""
        b = tk.Button(
            self,
            text=str(char),
            command=lambda: self.insert_character(char),
            width=6,
            background="#23D085",
            )
        b.grid(column=c, row=r, sticky="nsew")

    def create_keyboard_button(self, r, c, kboard):
        """Helper method that creates buttons that switch the keyboard"""
        b = tk.Button(
            self,
            text=str(kboard),
            command=lambda: self.switch_keyboard(kboard),
            background="gray",
            foreground="black"
            )
        b.grid(row=r, column=c, sticky="nsew")
        return b

    def insert_character(self, char):
        """Inserts char to the textbox"""
        self.text_box.config(state="normal")
        self.text_box.insert(tk.CURRENT, str(char))
        self.text_box.config(state="disabled")


root = tk.Tk()
app = alph_aerobics(master=root)
app.mainloop()

import os
from tkinter.messagebox import showerror
from tkinter.filedialog import (
    Text,
    Menu,
    Scrollbar,
    N,
    E,
    S,
    W,
    Y,
    Tk,
    askopenfilename,
    asksaveasfilename,
    RIGHT,
    END,
    TclError,
)

from reverse_writer import WordReverser




class Notepad:
    __root = Tk()

    # default window width and height
    __thisWidth = 300
    __thisHeight = 300
    __thisTextArea = Text(__root)
    __thisMenuBar = Menu(__root)
    __thisFileMenu = Menu(__thisMenuBar, tearoff=0)
    __thisEditMenu = Menu(__thisMenuBar, tearoff=0)
    __thisHelpMenu = Menu(__thisMenuBar, tearoff=0)

    # To add scrollbar
    __thisScrollBar = Scrollbar(__thisTextArea)
    __file = None

    def __init__(self, **kwargs):

        # Set window size (the default is 300x300)

        try:
            self.__thisWidth = kwargs["width"]
        except KeyError:
            pass

        try:
            self.__thisHeight = kwargs["height"]
        except KeyError:
            pass

        # Set the window text
        self.__root.title("Youthful-Yeomen : Untitled")

        # Center the window
        screen_width = self.__root.winfo_screenwidth()
        screen_height = self.__root.winfo_screenheight()

        # For left-align
        left = (screen_width / 2) - (self.__thisWidth / 2)

        # For right-align
        top = (screen_height / 2) - (self.__thisHeight / 2)

        # For top and bottom
        self.__root.geometry(
            "%dx%d+%d+%d" % (self.__thisWidth, self.__thisHeight, left, top)
        )

        # To make the text area auto resizable
        self.__root.grid_rowconfigure(0, weight=1)
        self.__root.grid_columnconfigure(0, weight=1)

        # Add controls (widget)
        self.__thisTextArea.grid(sticky=N + E + S + W)
        wr = WordReverser()
        self.__thisTextArea.bind("<KeyRelease>", wr.reverse_word_only)
        # To open new file
        self.__thisFileMenu.add_command(label="New", command=self.__new_file)

        # To open a already existing file
        self.__thisFileMenu.add_command(label="Open", command=self.__open_file)

        # To save current file
        self.__thisFileMenu.add_command(label="Save", command=self.__save_file)

        # To create a line in the dialog
        self.__thisFileMenu.add_separator()
        self.__thisFileMenu.add_command(label="Exit",
                                        command=self.__quit_application)
        self.__thisMenuBar.add_cascade(label="File", menu=self.__thisFileMenu)

        # To give a feature of cut
        self.__thisEditMenu.add_command(label="Cut", command=self.__cut)

        # to give a feature of copy
        self.__thisEditMenu.add_command(label="Copy", command=self.__copy)

        # To give a feature of paste
        self.__thisEditMenu.add_command(label="Paste", command=self.__paste)

        # to give a feature of reverse
        self.__thisEditMenu.add_command(label="Reverse", command=self.__reverse)

        # To give a feature of editing
        self.__thisMenuBar.add_cascade(label="Edit", menu=self.__thisEditMenu)

        self.__root.config(menu=self.__thisMenuBar)

        self.__thisScrollBar.pack(side=RIGHT, fill=Y)

        # Scrollbar will adjust automatically according to the content
        self.__thisScrollBar.config(command=self.__thisTextArea.yview)
        self.__thisTextArea.config(yscrollcommand=self.__thisScrollBar.set)

    def __quit_application(self):
        self.__root.destroy()

    def __open_file(self):

        self.__file = askopenfilename(
            defaultextension=".txt",
            filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")],
        )

        if self.__file == "":

            # no file to open
            self.__file = None
        else:

            self.__root.title(
                os.path.basename(self.__file) + " - Youthful-Yeomen")
            self.__thisTextArea.delete(1.0, END)

            file = open(self.__file, "r")
            reversed_file = file.read()[::-1]

            self.__thisTextArea.insert(1.0, reversed_file)

            file.close()

    def __new_file(self):
        self.__root.title("Youthful-Yeomen : Untitled")
        self.__file = None
        self.__thisTextArea.delete(1.0, END)

    def __save_file(self):

        if self.__file is None:
            # Save as new file
            self.__file = asksaveasfilename(
                initialfile="Untitled.txt",
                defaultextension=".txt",
                filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")],
            )

            if self.__file == "":
                self.__file = None
            else:

                # Try to save the file
                file = open(self.__file, "w")
                file.write(self.__thisTextArea.get(1.0, END))
                file.close()

                # Change the window title
                self.__root.title(os.path.basename(self.__file) + " - Notepad")

        else:
            file = open(self.__file, "w")
            file.write(self.__thisTextArea.get(1.0, END))
            file.close()

    def __cut(self):
        self.__thisTextArea.event_generate("<<Cut>>")

    def __copy(self):
        self.__thisTextArea.event_generate("<<Copy>>")

    def __paste(self):
        self.__thisTextArea.event_generate("<<Paste>>")

    def __reverse(self):
        try:
            text = self.__thisTextArea.get('sel.first', 'sel.last')
        except TclError:
            showerror(title="Error", message="Please select text to reverse")
            return
        reversed_text = text[::-1]
        self.__thisTextArea.insert('sel.first', reversed_text)
        self.__thisTextArea.delete('sel.first', 'sel.last')

    def run(self):
        self.__root.mainloop()

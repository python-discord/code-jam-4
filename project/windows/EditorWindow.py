import tkinter as tk
from tkinter import filedialog


class EditorWindow(tk.Toplevel):
    """
    This class houses the main text editor window.
    """

    def __init__(self, master):
        super().__init__(master)

        # Setting up grid options so that the text box stretches.
        tk.Grid.rowconfigure(self, index=0, weight=1)
        tk.Grid.columnconfigure(self, index=0, weight=1)

        # Setting up the main text entry in the window.
        self.text_box = tk.Text(self)
        self.text_box.grid(row=0, column=0, sticky=tk.NSEW)

        # Setting up the menu bar up the top.
        self.menu_bar = EditorMenuBar(self)

    def get_text(self) -> str:
        """
        A method other objects can use to retrieve the text inside
        the editor window's text box.

        :return: The text inside the editor window's text box.
        """
        return self.text_box.get("1.0", tk.END)

    def set_text(self, value):
        """
        A method other objects can use to alter the text inside the
        editor window's text box
        """
        self.text_box.delete(1.0, tk.END)
        self.text_box.insert(tk.END, value)


class EditorMenuBar(tk.Menu):
    """
    This class represents the menu bar in the editor window.
    """
    def __init__(self, master: EditorWindow):
        super().__init__(master)

        # A named reference to the editor window containing this menu bar.
        # It will be used in command callbacks to interact with the editor
        # window.
        self.editor_window = master

        # Adding the individual menus to the menu bar.
        self.file_menu = EditorFileMenu(self)
        self.edit_menu = EditorEditMenu(self)
        self.help_menu = EditorHelpMenu(self)

        # Setting self as the window's menu bar.
        master.config(menu=self)


class EditorMenu(tk.Menu):
    """
    This class represents an individual menu in the editor window's menu bar.
    """

    # The name with which this menu should be added to the menu bar.
    name = None

    # A type annotation for IDE auto-completion purposes.
    master: EditorMenuBar

    def __init__(self, master: EditorMenuBar):
        super().__init__(master, tearoff=False)

        # Adding self to the menu bar.
        self.master.add_cascade(label=self.name, menu=self)


class EditorFileMenu(EditorMenu):
    """
    This class represents the File menu in the editor window's menu bar.
    """

    name = 'File'

    def __init__(self, master: EditorMenuBar):
        super().__init__(master)

        # Setting up individual commands in the menu.
        self.add_command(label='Open', command=self.on_open)
        self.add_command(label='Save', command=self.on_save)
        # self.add_command(label='Save As', command=self.on_save_as)

    def on_open(self):
        """
        Called when the 'Open' action is selected from the File menu.
        """

        # Brings up a dialog asking the user to select a location for saving
        # the file.
        file = filedialog.askopenfile(
            filetypes=(('Text Files', '*.txt'), ('All Files', '*.*'))
        )

        # Check to see if the user cancelled the dialog or not.
        if file:
            # 'with' is used so that the file is automatically flushed/closed
            # after our work is done with it.
            with file:
                self.master.editor_window.set_text(file.read())

    def on_save(self):
        """
        Called when the 'Save' action is selected from the File menu.
        """

        # Brings up a dialog asking the user to select a location for saving
        # the file.
        file = filedialog.asksaveasfile(
            filetypes=(('Text Files', '*.txt'), ('All Files', '*.*'))
        )

        # Check to see if the user cancelled the dialog or not.
        if file:
            # 'with' is used so that the file is automatically flushed/closed
            # after our work is done with it.
            with file:
                file.write(self.master.editor_window.get_text())

    # def on_save_as(self):
    #     """
    #     Called when the 'Save As' action is selected from the File menu.
    #     """

    #     pass


class EditorEditMenu(EditorMenu):
    """
    This class represents the File menu in the editor window's menu bar.
    """

    name = 'Edit'

    def __init__(self, master: EditorMenuBar):
        super().__init__(master)

        # Setting up individual commands in the menu.
        self.add_command(label='Copy', command=self.on_copy)
        self.add_command(label='Cut', command=self.on_cut)
        self.add_command(label='Paste', command=self.on_paste)

    def on_copy(self):
        """
        Called when the 'Copy' action is selected from the Edit menu.
        """

        pass

    def on_cut(self):
        """
        Called when the 'Cut' action is selected from the Edit menu.
        """

        pass

    def on_paste(self):
        """
        Called when the 'Paste' action is selected from the Edit menu.
        """

        pass


class EditorHelpMenu(EditorMenu):
    """
    This class represents the Help menu in the editor window's menu bar.
    """

    name = 'Help'

    def __init__(self, master: EditorMenuBar):
        super().__init__(master)

        # Setting up individual commands in the menu.
        self.add_command(label='About', command=self.on_about)

    def on_about(self):
        """
        Called when the 'About' action is selected from the Help menu.
        """

        pass

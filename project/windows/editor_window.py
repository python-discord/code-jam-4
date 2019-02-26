import tkinter as tk
from tkinter import filedialog
from typing import Tuple

from project.windows.editor_window_events import NewWordEvent
from project.functionality.constants import Constants

# TODO: Fix docstring inconsistencies. Some have param docs, some don't etc.


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

        # Setting up the menu bar at the top.
        self.menu_bar = EditorMenuBar(self)

        # Set up scrollbar on the right hand side.
        self.scroll_bar = tk.Scrollbar(self, command=self.text_box.yview)
        self.text_box.config(yscrollcommand=self.scroll_bar.set)
        self.scroll_bar.grid(row=0, column=1, sticky=tk.NS)

        # Setting up the 'new word' event. This gets emitted every time the
        # user is detected to have typed a word.
        #
        # Callbacks can be assigned to be invoked when this event occurs using
        # new_word.add_callback(). Data will be passed to the callbacks inside
        # a NewWordEventData object. These objects contain information about
        # the start index, end index and contents of the typed word. The class
        # definitions for NewWordEvent and NewWordEventData are inside
        # project/windows/editor_window_events.py.
        #
        # There is an example of how to work with this event in
        # testing/test_editor_window.py
        self.new_word = NewWordEvent()

        # Setting up key press event binding.
        self.text_box.bind('<Key>', self.on_key_press)

        # Setting up right click event binding.
        self.text_box.bind('<Button-3>', self.on_right_click)

        # Setting up editing function key event binding.
        self.text_box.bind('<Control-C>', self.menu_bar.edit_menu.on_copy)
        self.text_box.bind('<Control-X>', self.menu_bar.edit_menu.on_cut)
        self.text_box.bind('<Control-V>', self.menu_bar.edit_menu.on_paste)

        # Set window title.
        self.wm_title('Editor')

    def get_text(self, start='1.0', end=tk.END) -> str:
        """
        A method other objects can use to retrieve the text inside
        the editor window's text box. By default it'll get all text inside the
        text box, but start and end values can also be specified.

        :param start: The starting index of the content to retrieve.
        :param end: The ending index of the content to retrieve. Pass None to
                    get a single character.
        :return: The text inside the editor window's text box.
        """

        return self.text_box.get(start, end)

    def set_text(self, value, start='1.0', end=tk.END, *tags):
        """
        A method other objects can use to alter the text inside the
        editor window's text box. By default it'll set all text inside the
        text box, but start and end values can also be specified.

        :param value: The value to set the text to.
        :param start: The starting index of the content to set.
        :param end: The ending index of the content to set.
                    Pass None to set a single character.
        :param tags: The tags to add to the changed content.
        """

        self.text_box.delete(start, end)
        self.text_box.insert(start, value, *tags)

    def get_selected_text(self) -> str:
        """
        A method other objects can use to retrieve the selected text inside
        the editor window's text box.

        :return: The selected text inside the editor window's text box.
                 If no text is selected, an empty string is returned instead.
        """

        try:
            return self.text_box.get(tk.SEL_FIRST, tk.SEL_LAST)

        except tk.TclError:
            return ''

    def set_selected_text(self, value, set_selected=True):
        """
        A method other objects can use to alter the selected text inside the
        editor window's text box.

        If no text is selected, the passed value is inserted at the current
        cursor position instead.

        If set_selected is True, then the set text will be selected. Otherwise
        it'll be normal.
        """

        try:
            insert_position = self.text_box.index(tk.SEL_FIRST)
            self.text_box.delete(tk.SEL_FIRST, tk.SEL_LAST)

        except tk.TclError:
            insert_position = tk.INSERT

        if set_selected:
            self.text_box.insert(insert_position, value, tk.SEL)
        else:
            self.text_box.insert(insert_position, value)

    def get_selection_indexes(self) -> Tuple[str, str]:
        """
        Retrieves the start and end indexes of the current selected text.
        If no text is selected, returns two empty strings.

        :return: The indexes on the current selected text. If no text is
                 selected, returns two empty strings.
        """

        try:
            return (
                self.text_box.index(tk.SEL_FIRST),
                self.text_box.index(tk.SEL_LAST)
            )

        except tk.TclError:
            return '', ''

    def set_selection_indexes(self, start, end):
        """
        Selects the text between two indexes.

        TODO: Test this method.

        :param start: The starting index of the selected text.
        :param end: The ending index of the selected text.
                    Pass None to set a single character.
        """

        self.text_box.tag_add(tk.SEL, start, end)

    def get_word_at_text_box_index(self, index) -> Tuple[str, str, str]:
        """
        Returns the word containing the character located at index.
        If the character is a space or not part of a word (not alphabetic) an
        empty string is returned instead.

        :return: The word containing the character located at index, or an
                 empty string if the character is a space or not part of a
                 word (not alphabetic).
        """

        line, character = map(int, index.split('.'))

        start = character
        end = character

        # Find position of first space before index.
        while start > 0:
            current_character: str = self.text_box.get(
                f'{line}.{start - 1}'
            )

            if not current_character.isalpha():
                break
            else:
                start -= 1

        # Find position of first space after index.
        while True:
            current_character: str = self.text_box.get(
                f'{line}.{end}'
            )

            if not current_character.isalpha():
                break

            end += 1

        start = f'{line}.{start}'
        end = f'{line}.{end}'

        return (
            start, end,
            self.text_box.get(start, end)
        )

    def get_word_at_text_box_pixel_position(self, x, y):
        """
        Returns the word closest to pixel position x, y in the editor window's
        text box, starting from 0, 0 at the top left.

        :return: The word closest to pixel position x, y in the editor window's
                 text box.
        """

        return self.get_word_at_text_box_index(
            self.text_box.index(f'@{x},{y}')
        )

    def get_word_under_mouse(self):
        """
        Gets the current word in the editor window's text box closest to the
        mouse pointer.

        If the mouse isn't over a word it will return an empty string.

        :return: Current word in the editor window's text box closest to the
                 mouse pointer, or an empty string if the mouse isn't over a
                 word.
        """

        return self.get_word_at_text_box_index(
            self.text_box.index(tk.CURRENT)
        )

    def on_key_press(self, event):
        """
        Called every time the user presses a key while focused on the editor
        window's text box.
        By default it handles detecting when the user types a word and firing
        the new_word event to signal this.

        :param event: tkinter event data
        """

        # TODO: This needs improvement. Checking the current index isn't a
        #       reliable way to handle this I think. Not sure if the key press
        #       and index change are always properly synchronized.

        if (
                event.char and
                not event.char.isalpha() and
                event.char != '\x08'
        ):
            for flag in Constants.forbidden_flags:
                if event.state & flag:
                    break
            else:
                previous_character: str = self.text_box.get(f'{tk.INSERT}-1c')
                if previous_character.isalpha():
                    start, end, word = self.get_word_at_text_box_index(
                        self.text_box.index(f'{tk.INSERT}-1c')
                    )

                    self.new_word(start, end, word)

    def on_right_click(self, event):
        """
        Called when the user right clicks over the editor window's text box.
        By default it creates and shows a context menu at the position of the
        mouse.

        :param event: tkinter event data passed
        """

        # Create a new context menu.
        context_menu = EditorContextMenu(self)

        # If there is selected text, add Cut and Copy options to the context
        # menu.
        selected_text = self.get_selected_text()
        if selected_text:
            context_menu.add_command(
                label='Cut', command=self.menu_bar.edit_menu.on_cut
            )

            context_menu.add_command(
                label='Copy', command=self.menu_bar.edit_menu.on_copy
            )

        context_menu.add_command(
            label='Paste', command=self.menu_bar.edit_menu.on_paste
        )

        context_menu.show()


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
        self.add_separator()
        self.add_command(label='Exit', command=self.on_exit)

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

    def on_exit(self):
        self.master.editor_window.destroy()


class EditorEditMenu(EditorMenu):
    """
    This class represents the File menu in the editor window's menu bar.
    """

    name = 'Edit'

    def __init__(self, master: EditorMenuBar):
        super().__init__(master)

        # Setting up individual commands in the menu.
        self.add_command(label='Cut', command=self.on_cut)
        self.add_command(label='Copy', command=self.on_copy)
        self.add_command(label='Paste', command=self.on_paste)

    def on_cut(self):
        """
        Called when the 'Cut' action is selected from the Edit menu.
        """

        root: tk.Tk = self.master.editor_window.master
        root.clipboard_clear()
        root.clipboard_append(
            self.master.editor_window.get_selected_text()
        )
        self.master.editor_window.set_selected_text('')

    def on_copy(self):
        """
        Called when the 'Copy' action is selected from the Edit menu.
        """

        root: tk.Tk = self.master.editor_window.master
        root.clipboard_clear()
        root.clipboard_append(
            self.master.editor_window.get_selected_text()
        )

    def on_paste(self):
        """
        Called when the 'Paste' action is selected from the Edit menu.
        """

        root: tk.Tk = self.master.editor_window.master
        try:
            self.master.editor_window.set_selected_text(
                root.clipboard_get(),
                set_selected=False
            )

        except tk.TclError:
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

        # TODO: Implement About dialog.
        pass


class EditorContextMenu(tk.Menu):
    """
    This class represents a context menu appearing over an editor window's
    text box.
    """

    def __init__(self, master):
        super().__init__(master, tearoff=False)

    def show(self):
        self.tk_popup(*self.winfo_pointerxy())

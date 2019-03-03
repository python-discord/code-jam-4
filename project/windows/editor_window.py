from typing import Tuple

import tkinter as tk

from tkinter import filedialog

from project.functionality.constants import Constants
from project.functionality.utility import pairwise

from project.windows.editor_window_events import NewWordEvent, NewWordEventData

from project.windows.cloppy_window import cloppy_yesno, CloppyButtonWindow
from project.windows.cloppy_window_events import CloppyChoiceMadeEventData

from project.windows.cloppy_spelling_window import CloppySpellingWindow

from project.spelling.correction import is_correct


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

        # Register the on_new_word callback for the new_word event.
        self.new_word.add_callback(self.on_new_word)

        # Setting up key press event binding.
        self.text_box.bind('<Key>', self.on_key_press)

        # Setting up right click event binding.
        self.text_box.bind('<Button-3>', self.on_right_click)

        # Setting up editing function key event binding.
        self.text_box.bind('<Control-x>', self.on_control_x)
        self.text_box.bind('<Control-c>', self.on_control_c)
        self.text_box.bind('<Control-v>', self.on_control_v)

        # Setting up saving and opening key event binding.
        self.text_box.bind('<Control-s>', self.on_control_s)
        self.text_box.bind('<Control-o>', self.on_control_o)

        # Setting up new file key event binding.
        self.text_box.bind('<Control-n>', self.on_control_n)

        # Setting up backspace/delete key event binding.
        self.text_box.bind('<BackSpace>', self.on_backspace)
        self.text_box.bind('<Delete>', self.on_backspace)

        # Set window title.
        self.wm_title(Constants.program_name)

        # Setting up window destruction event binding.
        self.protocol('WM_DELETE_WINDOW', self.on_destroy)
        # self.bind('<Destroy>', lambda e: None)

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

        :param value: The new value of the selected text.
        :param set_selected: If true, the new text will also be selected.
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

        :param index: The index of a letter in the the text box.

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

            if not (current_character.isalpha() or current_character == "'"):
                break
            else:
                start -= 1

        # Find position of first space after index.
        while True:
            current_character: str = self.text_box.get(
                f'{line}.{end}'
            )

            if not (current_character.isalpha() or current_character == "'"):
                break

            end += 1

        word = self.text_box.get(f'{line}.{start}', f'{line}.{end}')

        # Correct indexes with regards to leading and trailing apostrophes.
        start_offset = 0
        end_offset = 0

        for character in word:
            if character == "'":
                start_offset += 1
            else:
                break

        for character, next_character in pairwise(reversed(word)):
            if character == "'":
                if next_character:
                    if next_character.lower() != 's':
                        end_offset -= 1
                else:
                    end_offset -= 1
                    break
            else:
                break

        start += start_offset
        word = word[start_offset:]

        if end_offset:
            end += end_offset
            word = word[:end_offset]

        start = f'{line}.{start}'
        end = f'{line}.{end}'

        return start, end, word

    def get_word_at_text_box_pixel_position(self, x, y):
        """
        Returns the word closest to pixel position x, y in the editor window's
        text box, starting from 0, 0 at the top left.

        :param x: Position on the text box along the x axis, from top to
                  bottom.
        :param y: Position on the text box along the y axis, from up to down.

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

        :return: A tuple containing the starting index, ending index and
                 content of the word in the text box closest the mouse cursor.
        """

        return self.get_word_at_text_box_index(
            self.text_box.index(tk.CURRENT)
        )

    def delete_selected_text(self, backspace=True):
        """
        Deletes any selected text.
        If nothing is selected, and backspace is set to True, then deletes the
        character behind the cursor.

        :param backspace: If True, when no text is selected, the character
                          behind the cursor is deleted instead.
        """
        selected_start, selection_end = self.get_selection_indexes()
        if selected_start and selection_end:
            self.set_selected_text('', False)

        elif backspace:
            if self.text_box.index(tk.INSERT) != '1.0':
                self.set_text('', f'{tk.INSERT}-1c', None)

    def on_key_press(self, event):
        """
        Called every time the user presses a key while focused on the editor
        window's text box.
        By default it handles detecting when the user types a word and firing
        the new_word event to signal this.

        :param event: tkinter event data
        """

        if (
            event.char and
            not event.char.isalpha() and
            event.char != "'" and
            event.char != '\x08'  # backspace
        ):
            for flag in Constants.forbidden_flags:
                if event.state & flag:
                    break
            else:
                previous_character: str = self.text_box.get(f'{tk.INSERT}-1c')
                if previous_character.isalpha() or previous_character == "'":
                    start, end, word = self.get_word_at_text_box_index(
                        self.text_box.index(f'{tk.INSERT}-1c')
                    )

                    self.new_word(start, end, word)

    def on_backspace(self, event):
        """
        Called when the backspace key is pressed in the editor's text box.

        :param event: tkinter event data
        :return: 'break' in order to interrupt the normal event handling of
                 the backspace key.
        """

        def delete_text(choice_data: CloppyChoiceMadeEventData):
            if choice_data.choice == 'Yes':
                self.delete_selected_text()

        cloppy_yesno(
            self,
            "It looks like you're trying to erase some text.\n"
            "The text you're erasing could be very important.",
            delete_text
        ).show()

        return 'break'

    def on_control_x(self, event=None):
        """
        Called when Ctrl+X is pressed in the editor's text box.
        Also called by the 'Cut' menu options.

        :param event: tkinter event data. None by default in case the method
                      is invoked artificially.
        :return: 'break' in order to interrupt the normal event handling of
                 the backspace key.
        """

        def cut_text(choice_data: CloppyChoiceMadeEventData):
            if choice_data.choice == 'Yes':
                root: tk.Tk = self.master
                root.clipboard_clear()
                root.clipboard_append(
                    self.get_selected_text()
                )
                self.set_selected_text('')

        cloppy_yesno(
            self,
            "It looks like you're trying to cut some text.\n"
            "The text you're erasing could be very important.",
            cut_text
        ).show()

        return 'break'

    def on_control_c(self, event=None):
        """
        Called when Ctrl+C is pressed in the editor's text box.
        Also called by the 'Copy' menu options.

        :param event: tkinter event data. None by default in case the method
                      is invoked artificially.
        :return: 'break' in order to interrupt the normal event handling of
                 the backspace key.
        """

        def copy_text(choice_data: CloppyChoiceMadeEventData):
            if choice_data.choice == 'Yes':
                root: tk.Tk = self.master
                root.clipboard_clear()
                root.clipboard_append(self.get_selected_text())

        cloppy_yesno(
            self,
            "It looks like you're trying to copy some text.\n"
            "You might not have highlighted the correct section to copy.\n"
            "Perhaps it'd be a good idea to double check now.",
            copy_text
        ).show()

        return 'break'

    def on_control_v(self, event=None):
        """
        Called when Ctrl+V is pressed in the editor's text box.
        Also called by the 'Paste' menu options.

        :param event: tkinter event data. None by default in case the method
                      is invoked artificially.
        :return: 'break' in order to interrupt the normal event handling of
                 ctrl+v.
        """

        def paste_text(choice_data: CloppyChoiceMadeEventData):
            if choice_data.choice == 'Yes':
                root: tk.Tk = self.master
                try:
                    self.set_selected_text(
                        root.clipboard_get(),
                        set_selected=False
                    )

                except tk.TclError:
                    pass

        cloppy_yesno(
            self,
            "It looks like you're trying to paste some text.\n"
            "The text you're pasting could be replacing other important text.",
            paste_text
        ).show()

        return 'break'

    def on_control_s(self, event=None):
        """
        Called when Ctrl+S is pressed in the editor's text box.
        Also called by the 'Save' menu option.

        :param event: tkinter event data. None by default in case the method
                      is invoked artificially.
        :return: 'break' in order to interrupt the normal event handling of
                 the backspace key.
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
                file.write(self.get_text())

        return 'break'

    def on_control_o(self, event=None):
        """
        Called when Ctrl+O is pressed in the editor's text box.
        Also called by the 'Open' menu option.

        :param event: tkinter event data. None by default in case the method
                      is invoked artificially.
        :return: 'break' in order to interrupt the normal event handling of
                 the backspace key.
        """

        # Cloppy asks the user whether they want to open a file.

        def open_file(choice_data: CloppyChoiceMadeEventData):
            if choice_data.choice == 'Yes':
                # Brings up a dialog asking the user to select a location for
                # saving the file.
                file = filedialog.askopenfile(
                    filetypes=(('Text Files', '*.txt'), ('All Files', '*.*'))
                )

                # Check to see if the user cancelled the dialog or not.
                if file:
                    # 'with' is used so that the file is automatically flushed
                    # /closed after our work is done with it.
                    with file:
                        self.set_text(file.read())

        cloppy_yesno(
            self,
            "It looks like you're trying to open a file.\n"
            "If you do you'll lose any unsaved work in the current file.",
            open_file
        ).show()

        return 'break'

    def on_control_n(self, event=None):
        """
        Called when Ctrl+N is pressed in the editor's text box.
        Also called by the 'New' menu option.

        :param event: tkinter event data. None by default in case the method
                      is invoked artificially.
        :return: 'break' in order to interrupt the normal event handling of
                 the backspace key.
        """

        # Cloppy asks the user whether they want to create a new file.
        def new_file(choice_data: CloppyChoiceMadeEventData):
            if choice_data.choice == 'Yes':
                self.set_text('')

        cloppy_yesno(
            self,
            "It looks like you're trying to create a new file.\n"
            "If you do you'll lose any unsaved work in the current file.",
            new_file
        ).show()

        return 'break'

    def on_right_click(self, event):
        """
        Called when the user right clicks over the editor window's text box.
        By default it creates and shows a context menu at the position of the
        mouse.

        :param event: tkinter event data
        :return: 'break' in order to interrupt the normal event handling of
                 right click.
        """

        # Create a new context menu.
        context_menu = EditorContextMenu(self)

        # If there is selected text, add Cut and Copy options to the context
        # menu.
        selected_text = self.get_selected_text()
        if selected_text:
            context_menu.add_command(
                label='Cut', command=self.on_control_x
            )

            context_menu.add_command(
                label='Copy', command=self.on_control_c
            )

        context_menu.add_command(
            label='Paste', command=self.on_control_v
        )

        context_menu.show()
        return 'break'

    def on_new_word(self, word_data: NewWordEventData):
        """
        Called every time a new word is typed in the editor's text box.
        :param word_data: An object containing information about the starting
                          index, ending index and contents of the word.
        """
        word_data.word = word_data.word.lower()
        if not is_correct(word_data.word.lower()):
            CloppySpellingWindow(self, word_data).show()

    def on_destroy(self):
        """
        Called whenever the window is about to be closed.

        :return: 'break' to interrupt the normal handling of any events this
                 method is bound to.
        """
        def destroy_window(choice_data: CloppyChoiceMadeEventData):
            if choice_data.choice == 'Yes':
                try:
                    self.master.destroy()

                except tk.TclError:
                    pass

        cloppy_yesno(
            self,
            "It looks like you're about to exit the program.\n"
            "If you do this you might lose any unsaved work.",
            destroy_window
        ).show()

        return 'break'


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

    def on_new(self):
        """
        Called when the 'New' action is selected from the File menu.
        """

        self.master.editor_window.on_control_n()

    def on_open(self):
        """
        Called when the 'Open' action is selected from the File menu.
        """

        self.master.editor_window.on_control_o()

    def on_save(self):
        """
        Called when the 'Save' action is selected from the File menu.
        """

        self.master.editor_window.on_control_s()

    # def on_save_as(self):
    #     """
    #     Called when the 'Save As' action is selected from the File menu.
    #     """

    #     pass

    def on_exit(self):
        """
        Called when the user selects the 'Exit' option in the File menu.
        """
        self.master.editor_window.on_destroy()


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

        self.master.editor_window.on_control_x()

    def on_copy(self):
        """
        Called when the 'Copy' action is selected from the Edit menu.
        """

        self.master.editor_window.on_control_c()

    def on_paste(self):
        """
        Called when the 'Paste' action is selected from the Edit menu.
        """

        self.master.editor_window.on_control_v()


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

        dialog = CloppyButtonWindow(self.master.editor_window)
        dialog.set_message(
            f'This program was made by:\n'
            f'LargeKnome, Hanyuone, and Meta\n'
        )
        dialog.add_choice('Ok')
        dialog.show()


class EditorContextMenu(tk.Menu):
    """
    This class represents a context menu appearing over an editor window's
    text box.
    """

    def __init__(self, master):
        super().__init__(master, tearoff=False)

    def show(self):
        self.tk_popup(*self.winfo_pointerxy())

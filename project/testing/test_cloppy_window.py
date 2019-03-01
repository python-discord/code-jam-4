# This file is used to test the editor window in isolation.
# It will be removed during release.

import tkinter as tk
from project.windows.editor_window import EditorWindow
from project.windows.cloppy_window import CloppyButtonWindow, CloppyInputWindow
from project.windows.editor_window_events import NewWordEventData
from project.windows.cloppy_window_events import CloppyChoiceMadeEventData


class TestEditorWindow(EditorWindow):
    """
    A version of the editor window specifically made for testing.
    """

    def __init__(self, master):
        super().__init__(master)

        # self.withdraw()

        self.text_box.tag_config('Underlined', underline=1)
        self.previous_word: NewWordEventData = None

        def underline_new_word(event_data: NewWordEventData):
            if self.previous_word:
                self.text_box.tag_remove(
                    'Underlined',
                    self.previous_word.start, self.previous_word.end
                )

            self.text_box.tag_add(
                'Underlined', event_data.start, event_data.end
            )

            self.previous_word = event_data

        self.new_word.add_callback(underline_new_word)

        self.text_box.bind('<Button-1>', self.on_left_click)

        def show_cloppy(event):
            # print('test')
            # new_window = CloppyButtonWindow(self)
            # new_window.set_message('test')
            # new_window.add_choice('test_choice')
            # new_window.add_choice('test_choice 2')
            # new_window.add_choice('test_choice 3')
            # new_window.add_choice('test_choice 4')

            new_window = CloppyInputWindow(self)

            def show_choice(data: CloppyChoiceMadeEventData):
                print(data.message, data.choice)
            new_window.choice_made.add_callback(show_choice)

            new_window.show()

        self.bind('<k>', show_cloppy)

    def on_left_click(self, event: tk.Event):
        start, end, word = self.get_word_under_mouse()
        if word:
            if self.previous_word:
                self.text_box.tag_remove(
                    'Underlined',
                    self.previous_word.start, self.previous_word.end
                )

            self.text_box.tag_add(
                'Underlined', start, end
            )

            self.previous_word = NewWordEventData(start, end, word)


if __name__ == '__main__':
    root = tk.Tk()

    # Hide root window.
    root.withdraw()

    editor_window = TestEditorWindow(root)

    # This will close the hidden root window when the editor window is closed.
    editor_window.protocol('WM_DELETE_WINDOW', root.destroy)

    root.mainloop()

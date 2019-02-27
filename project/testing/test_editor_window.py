# This file is used to test the editor window in isolation.
# It will be removed during release.

import tkinter as tk
from project.windows.editor_window import EditorWindow, EditorContextMenu
from project.windows.editor_window_events import NewWordEventData


class TestEditorWindow(EditorWindow):
    """
    A version of the editor window specifically made for testing.
    """

    def __init__(self, master):
        super().__init__(master)

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

        self.bind('<Button-1>', self.on_left_click)
        # self.test_button = tk.Button(
        #     master=self,
        #     text='test',
        #     command=self.test
        # )

        # self.test_button.grid(row=1, column=0, sticky=tk.NSEW)

        # self.text_box.bind('<Button-3>', self.test)

    # def test(self, *args):
    #     pass
    #     # print(self.get_text())
    #     # print(f'"{self.get_word_under_mouse()}"')
    #     # context_menu = EditorContextMenu(self)
    #     # context_menu.show()

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

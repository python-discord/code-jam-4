# this file will only be used to test the editor window and will be removed during release.

import tkinter as tk
from project.windows.EditorWindow import EditorWindow

if __name__ == '__main__':
    root = tk.Tk()
    editor_window = EditorWindow(root)
    editor_window.mainloop()

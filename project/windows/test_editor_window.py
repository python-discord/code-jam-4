# This file is used to test the editor window in isolation.
# It will be removed during release.

import tkinter as tk
from project.windows.EditorWindow import EditorWindow

if __name__ == '__main__':
    root = tk.Tk()

    # Hide root window.
    root.withdraw()

    editor_window = EditorWindow(root)

    # This will close the hidden root window when the editor window is closed.
    editor_window.protocol('WM_DELETE_WINDOW', root.destroy)

    root.mainloop()

import tkinter as tk
from project.windows.editor_window import EditorWindow

if __name__ == '__main__':
    root = tk.Tk()

    # Hide root window.
    root.withdraw()

    editor_window = EditorWindow(root)

    # This will close the hidden root window when the editor window is closed.
    editor_window.protocol('WM_DELETE_WINDOW', root.destroy)

    root.mainloop()

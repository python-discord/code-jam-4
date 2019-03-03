import tkinter as tk
from project.windows.editor_window import EditorWindow

if __name__ == '__main__':
    root = tk.Tk()

    # Hide root window.
    root.withdraw()

    # Create editor window.
    editor_window = EditorWindow(root)

    root.mainloop()

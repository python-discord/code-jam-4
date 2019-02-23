import tkinter as tk


class EditorWindow(tk.Frame):
    """
    This class houses the main text editor window.
    """

    def __init__(self, master):
        super().__init__(master)

        # The main text entry in the window.
        self.text_box = tk.Text(master)
        self.text_box.pack()

    def get_text(self) -> str:
        """
        A public method other objects can use to retrieve the text inside the editor window's text box.
        :return: The text inside the editor window's text box.
        """
        return self.text_box.get("1.0", tk.END)

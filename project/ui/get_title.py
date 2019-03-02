from random import shuffle
from PySide2.QtWidgets import QWidget
from .ui_files.ui_add_title import Ui_title_form


class AddTitle(QWidget, Ui_title_form):
    """
    Class containing the window for getting the Title of a Task.

    Attributes:
        width (int): Width of the window
        height (int): Height of the window
        task (dict): The task to load the title into.
            Format: {
                "Title": "Eat water",
                "Description": "Eat chunky water",
                "Deadline": 9999999991,
            }
        label_text (list of str): The list of characters in the title to be added.
        available_text (list of str): The list of characters corresponding to the
            current slider position.
        buttons (list of object): The QPushButton objects in the window.
    """

    def __init__(self, task):
        super().__init__()
        self.width, self.height = 600, 500
        self.task = task
        self.label_text = []

        self.init_UI()
        self.available_text = list((
            "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
            " 0123456789"
            "!@#$(),./?:\"'"
        ))

        self.buttons = [getattr(self, i)
                        for i in vars(self) if i.endswith("button")]
        self.bind_buttons()
        self.update()

    def init_UI(self):
        """
        Load the .ui-converted .py file, set the size and display the window.
        """
        self.setupUi(self)
        self.setFixedSize(self.width, self.height)
        self.show()

    def randomize_text(self):
        """
        Randomizes the guide text.
        """
        shuffle(self.available_text)

    def bind_buttons(self):
        """
        Binds each button to their respective functions.
        """
        for button in self.buttons:
            func_dict = {
                "add_button": self.add,
                "delete_button": self.delete,
                "done_button": self.done,
            }
            button.clicked.connect(func_dict[button.objectName()])
            if button.objectName() != "done_button":
                button.clicked.connect(self.update)

    def add(self):
        """
        Adds the character corresponding to the current slider position to the
        label text.
        """

        to_add = self.available_text[self.text_slider.sliderPosition()]
        self.label_text.append(to_add)

    def delete(self):
        """
        Removes a character from the label text.
        """
        if self.label_text:
            self.label_text.pop()

    def update(self):
        """
        Update the display label text and guide text.
        """
        self.label.setText("".join(self.label_text))
        self.randomize_text()
        self.reference_label.setText("".join(reversed(self.available_text)))

    def done(self):
        """
        Sets the title of Task to the string in the label. Closes Window.
        """
        self.task["Title"] = "".join(self.label_text)
        self.close()

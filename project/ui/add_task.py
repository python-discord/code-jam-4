from random import randint, shuffle
from collections import namedtuple

from PySide2.QtWidgets import QWidget

from .ui_files.ui_add_task import Ui_task_form
from .get_title import AddTitle
from .get_desc import AddDesc
from .get_deadline import AddDeadline


class AddTask(QWidget, Ui_task_form):
    """
    Class containing the window for Adding a Task.

    Attributes:
        width (int): Width of the window
        height (int): Height of the window
        windows (list of object): A list of windows opened so they do not get
            garbage collected
        task (dict): The task to be added.
            Format: {
                "Title": "Eat water",
                "Description": "Eat chunky water",
                "Deadline": 9999999991,
            }
    """

    def __init__(self):
        super().__init__()
        self.width, self.height = 600, 500

        self.init_UI()
        self.bind_buttons()
        self.windows = []
        self.task = {}

    def init_UI(self):
        """
        Load the .ui-converted .py file, set the size and display the window.
        """
        self.setupUi(self)
        self.setFixedSize(self.width, self.height)

        self.buttons = [i for i in vars(self) if i.endswith("button")]
        self.button_text = ["Add Title",
                            "Add Deadline", "Done", "Add Description"]
        self.move_buttons()

        self.show()

    def randomize_names(self):
        """
        Randomizes the names of the buttons. The tooltip remains unchanged.
        """
        shuffle(self.button_text)
        for index, txt in enumerate(self.buttons):
            getattr(self, txt).setText(self.button_text[index])

    def move_buttons(self):
        """
        Moves the buttons to a random position in the window without overlapping.
        """
        def overlap(box_1, box_2):
            """
            Checks if two boxes overlap.

            Args:
                box_1 (namedtuple: int, int, int, int): The first box
                box_2 (namedtuple: int, int, int, int): The second box

            Returns:
                bool: True if the boxes overlap each other. False otherwise.
            """
            return (box_1.x1 < box_2.x2 and box_2.x1 < box_1.x2) and (
                box_1.y1 < box_2.y2 and box_2.y1 < box_1.y2)

        max_x, max_y = self.width - 250, self.height - 25

        Box = namedtuple("Box", ["x1", "x2", "y1", "y2"])
        boxes = []

        for txt in self.buttons:
            while True:
                rand_x, rand_y = randint(0, max_x), randint(
                    0, max_y)  # random position
                cur_box = Box(rand_x, rand_x + 250, rand_y, rand_y + 25)

                if any(overlap(cur_box, box) for box in boxes):
                    # Retry if box overlaps any other box already set
                    continue
                else:
                    getattr(self, txt).move(rand_x, rand_y)
                    boxes.append(cur_box)
                    break

    def bind_buttons(self):
        """
        Binds each button to their respective functions.
        """
        func_dict = {
            "form_title_button": self.get_title,
            "form_desc_button": self.get_desc,
            "form_date_button": self.get_date,
            "form_done_button": self.done,
        }
        for txt in self.buttons:
            button = getattr(self, txt)
            # execute function
            button.clicked.connect(func_dict[txt])
            # randomize button positions
            button.clicked.connect(self.move_buttons)
            # randomize button names
            button.clicked.connect(self.randomize_names)

    def get_title(self):
        form = AddTitle(self.task)
        self.windows.append(form)

    def get_desc(self):
        form = AddDesc(self.task)
        self.windows.append(form)

    def get_date(self):
        form = AddDeadline(self.task)
        self.windows.append(form)

    def done(self):
        print(self.task)

from PySide2.QtWidgets import QWidget
from .ui_files.ui_add_desc import Ui_desc_form


class AddDesc(QWidget, Ui_desc_form):
    def __init__(self, task):
        super().__init__()
        self.width, self.height = 600, 500
        self.task = task
        self.label_text = []

        self.init_UI()

        self.buttons = [i for i in vars(self) if i.endswith("button")]
        self.bind_buttons()

    def init_UI(self):
        self.setupUi(self)
        self.setFixedSize(self.width, self.height)
        self.show()

    def bind_buttons(self):
        for txt in self.buttons:
            func_dict = {
                "add_button": self.add,
                "delete_button": self.delete,
                "done_button": self.done,
            }
            button = getattr(self, txt)
            button.clicked.connect(func_dict[txt])
            if txt != "done_button":
                button.clicked.connect(self.update)

    def add(self):
        available_text = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        available_text += " 0123456789"
        available_text += "!@#$(),./?:\"'"

        to_add = available_text[self.text_slider.sliderPosition()]
        self.label_text.append(to_add)

    def delete(self):
        if self.label_text:
            self.label_text.pop()

    def update(self):
        self.label.setText("".join(self.label_text))

    def done(self):
        self.task["Description"] = "".join(self.label_text)
        self.close()

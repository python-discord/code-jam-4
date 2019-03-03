from PySide2.QtWidgets import QDialog

from project import ui


class RemoveDialogue(QDialog):
    def __init__(self, *args, **kwargs):
        super(RemoveDialogue, self).__init__(*args, **kwargs)

        self.ui = ui.RemoveDialogue()
        self.ui.setupUi(self)

        self.title = None

        self.ui.buttons.accepted.connect(self.accept)
        self.ui.buttons.rejected.connect(self.reject)

    def done(self, result: QDialog.DialogCode):
        if result == QDialog.Accepted:
            if self.title != self.ui.input.text():
                self.ui.input.setText(f"Incorrect, try again:")
                return

        self.ui.input.clear()
        self.ui.label.setText("Please enter the title of the media to confirm removal:")

        super().done(result)

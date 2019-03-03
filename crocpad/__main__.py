"""Entry point into the Crocpad++ application."""

import sys
from PyQt5.QtWidgets import QApplication
import crocpad.notepad

# By default PyQt5 will give crash messages like "Process finished with exit code 1"
# instead of a traceback. The following recipe to get tracebacks on an exception is from:
# https://stackoverflow.com/questions/34363552/python-process-finished-with-exit-code-1-when-using-pycharm-and-pyqt5

# BEGIN EXTERNAL CODE
# Back up the reference to the exception hook
sys._excepthook = sys.excepthook


def my_exception_hook(exctype, value, traceback):
    # Print the error and traceback
    print(exctype, value, traceback)
    # Call the normal Exception hook after
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)


# Set the exception hook to our wrapping function
sys.excepthook = my_exception_hook
# END EXTERNAL CODE

# Instantiate the application and main window, then pass control.
app = QApplication(sys.argv)
app.setApplicationName("Crocpad++")
window = crocpad.notepad.MainWindow(app)
app.exec_()

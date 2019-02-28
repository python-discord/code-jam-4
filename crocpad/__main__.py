import sys
from PyQt5.QtWidgets import QApplication
import crocpad.notepad

app = QApplication(sys.argv)
app.setApplicationName("Crocpad++")
window = crocpad.notepad.MainWindow()
app.exec_()

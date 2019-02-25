import sys

from PyQt5.QtGui import QFontDatabase, QIcon
from PyQt5.QtWidgets import (QApplication, QDesktopWidget, QMainWindow,
                             QMessageBox, QPlainTextEdit, QStatusBar,
                             QVBoxLayout, QWidget)


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        layout = QVBoxLayout()

        self.main_window = QPlainTextEdit()

        # Setup the QTextEdit editor configuration
        fixedfont = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        fixedfont.setPointSize(24)
        self.main_window.setFont(fixedfont)

        layout.addWidget(self.main_window)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.status = QStatusBar()
        self.setStatusBar(self.status)

        # Update title and centre window
        self.update_title()
        self.setGeometry(50, 50, 800, 600)
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())
        self.setWindowIcon(QIcon('crocpad.ico'))

        self.show()

    def dialog_critical(self, alert_text):
        dlg = QMessageBox(self)
        dlg.setText(alert_text)
        dlg.setIcon(QMessageBox.Critical)
        dlg.show()

    def update_title(self):
        self.setWindowTitle("Crocpad++")

    def edit_toggle_wrap(self):
        self.main_window.setLineWrapMode(not self.main_window.lineWrapMode())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName("Crocpad++")

    window = MainWindow()
    app.exec_()

import sys

from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtMultimedia import QSound
from PyQt5.QtGui import QFontDatabase, QIcon, QFont
from PyQt5.QtWidgets import (QApplication, QDesktopWidget, QMainWindow,
                             QMessageBox, QPlainTextEdit, QStatusBar,
                             QVBoxLayout, QWidget)
from configuration import app_config
from eula_dialog import EulaDialog


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        layout = QVBoxLayout()

        self.main_window = QPlainTextEdit()

        # Setup the QTextEdit editor configuration
        fixedfont = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        fixedfont.setPointSize(24)
        self.main_window.setFont(QFont('Comic Sans MS', 30))
        self.main_window.installEventFilter(self)
        self.sound = QSound("click.wav")
        self.enter_sound = QSound("scream.wav")
        self.backspace_sound = QSound("wrong.wav")

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
        self.setWindowIcon(QIcon('project\\crocpad.ico'))

        # Add Menus
        mainMenu = self.menuBar()
        helpMenu = mainMenu.addMenu('Help')
        viewMenu = mainMenu.addMenu('View')
        fileMenu = mainMenu.addMenu('Recent Files')
        editMenu = mainMenu.addMenu('Edit')
        searchMenu = mainMenu.addMenu('Search')
        toolsMenu = mainMenu.addMenu('Tools')

        # SubMenu Test
        testmenu = []
        for i in range(0, 200):
            testmenu.append(fileMenu.addMenu(f'{i}'))

        self.show()

        if app_config['License']['eulaaccepted'] != 'yes':
            with open('EULA.txt', 'r', encoding="utf8") as f:
                eula = f.read()
            self.eula_dialog = EulaDialog(eula)
            self.eula_dialog.exec_()
            if self.eula_dialog.clicked_button == self.eula_dialog.eula_agree_button:
                # We click the agree button
                pass

    def eventFilter(self, source, event):
        if event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
                self.sound.stop()
                self.enter_sound.play()
            if event.key() == Qt.Key_Backspace:
                self.sound.stop()
                self.backspace_sound.play()
            else:
                self.sound.play()
        return False

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

import random
import sys
from zipfile import BadZipFile

from PyQt5.QtCore import QEvent, Qt
from PyQt5.QtGui import QFont, QFontDatabase, QIcon
from PyQt5.QtMultimedia import QSound
from PyQt5.QtWidgets import (QAction, QApplication, QDesktopWidget,
                             QFileDialog, QMainWindow, QMessageBox,
                             QPlainTextEdit, QStatusBar, QVBoxLayout, QWidget)

from crocpad.configuration import app_config, save_config
from crocpad.eula_dialog import EulaDialog
from crocpad.eula_quiz_dialog import EulaQuizDialog


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
        self.sound = QSound("crocpad\\sounds\\click.wav")
        self.enter_sound = QSound("crocpad\\sounds\\scream.wav")
        self.backspace_sound = QSound("crocpad\\sounds\\wrong.wav")

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
        self.setWindowIcon(QIcon('crocpad\\crocpad.ico'))

        self.create_menus()

        self.show()

        if app_config['License']['eulaaccepted'] != 'yes':
            self.do_eula()

    def create_menus(self):
        mainMenu = self.menuBar()
        helpMenu = mainMenu.addMenu('H&elp')
        viewMenu = mainMenu.addMenu('Vi&ew')
        fileMenu = mainMenu.addMenu('R&ecent Files')
        editMenu = mainMenu.addMenu('&Edit')
        searchMenu = mainMenu.addMenu('S&earch')
        toolsMenu = mainMenu.addMenu('&Tools')

        action_open = QAction("S&earch for file to open", self)
        action_open.triggered.connect(self.open_file)
        searchMenu.addAction(action_open)
        action_save = QAction("S&earch for file to save", self)
        action_save.triggered.connect(self.save_file)
        searchMenu.addAction(action_save)
        action_new = QAction("S&earch for a new f&ile", self)
        action_new.triggered.connect(self.new_file)
        searchMenu.addAction(action_new)

        # SubMenu Test
        testmenu = []
        for i in range(0, 200):
            testmenu.append(fileMenu.addMenu(f'{i}'))

    def do_eula(self):
        with open('crocpad\\EULA.txt', 'r', encoding="utf8") as f:
            eula = f.read()
        self.eula_dialog = EulaDialog(eula)
        self.eula_quiz_dialog = EulaQuizDialog()
        while not self.eula_quiz_dialog.quiz_correct():
            self.eula_dialog.exec_()
            if self.eula_dialog.clicked_button == self.eula_dialog.eula_agree_button:
                # We click the agree button
                app_config['License']['eulaaccepted'] = 'yes'
                save_config(app_config)
            self.eula_quiz_dialog.exec_()

    def eventFilter(self, source, event):
        if event.type() == QEvent.KeyPress:
            if app_config['Sound']['sounds'] == 'on':
                if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
                    self.sound.stop()
                    self.enter_sound.play()
                if event.key() == Qt.Key_Backspace:
                    self.sound.stop()
                    self.backspace_sound.play()
                else:
                    self.sound.play()
            if event.key() == Qt.Key_Space:
                if random.random() > 0.8:
                    dlg = QMessageBox(self)
                    dlg.setWindowTitle("Are you sure?")
                    dlg.setText("_" * 100)
                    dlg.show()
                    dlg.close()
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

    def open_file(self):
        filename = QFileDialog.getOpenFileName()[0]
        with open(filename, 'r') as file:
            self.main_window.setPlainText(file.read())

    def save_file(self):
        filename = QFileDialog.getSaveFileName()[0]
        text = self.main_window.document().toPlainText()
        with open(filename, 'w') as file:
            file.write(text)

    def new_file(self):
        self.main_window.document().clear()
        self.main_window.insertPlainText("""To remove this message, please make sure you have entered
        your full credit card details, made payable to:
        Crocpad++ Inc
        PO BOX 477362213321233
        Cheshire Cheese
        Snekland
        Australia
        """
                                         )

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName("Crocpad++")

    window = MainWindow()
    app.exec_()

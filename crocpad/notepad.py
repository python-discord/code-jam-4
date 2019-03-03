"""The main module for Crocpad++.

Contains the application class MainWindow which should only be instantiated once.
"""

import random

from PyQt5.QtCore import QEvent, Qt, QObject
from PyQt5.QtGui import QFont, QFontDatabase, QIcon
from PyQt5.QtMultimedia import QSound
from PyQt5.QtWidgets import (QAction, QDesktopWidget, QApplication,
                             QFileDialog, QFontDialog, QMainWindow,
                             QMessageBox, QPlainTextEdit, QStatusBar,
                             QVBoxLayout, QWidget)

import crocpad.stylesheets
from crocpad.configuration import app_config, save_config
from crocpad.eula_dialog import EulaDialog
from crocpad.eula_quiz_dialog import EulaQuizDialog
from crocpad.insert_emoji_dialog import EmojiPicker


class MainWindow(QMainWindow):
    """Main application class for Crocpad++."""

    def __init__(self, app: QApplication, *args, **kwargs):
        """Set up the single instance of the application."""
        super(MainWindow, self).__init__(*args, **kwargs)
        self.app = app

        # Set up the QTextEdit editor configuration
        self.text_window = QPlainTextEdit()  # the actual editor pane
        fixedfont = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        fixedfont.setPointSize(24)
        self.text_window.setFont(QFont('Comic Sans MS', 30))
        self.text_window.installEventFilter(self)
        self.sound = QSound("crocpad\\sounds\\click.wav")
        self.enter_sound = QSound("crocpad\\sounds\\scream.wav")
        self.backspace_sound = QSound("crocpad\\sounds\\wrong.wav")

        # Main window layout. Most of the dialogs in Crocpad++ are converted to .py from
        # Qt Designer .ui files in the ui/ directory, but the main app window is built here.
        layout = QVBoxLayout()
        layout.addWidget(self.text_window)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        self.status = QStatusBar()
        self.setStatusBar(self.status)

        # Update title and centre window
        self.filename = "** Untitled **"
        self.update_title()
        self.setGeometry(50, 50, 800, 600)
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())
        self.setWindowIcon(QIcon('crocpad\\crocpad.ico'))
        self.create_menus()
        self.app.setStyleSheet(crocpad.stylesheets.default)
        self.show()

        # Post-startup tasks
        if app_config['License']['eulaaccepted'] != 'yes':
            self.do_eula()
        if app_config['Editor']['tips'] == 'on':
            self.show_tip()

    def create_menus(self):
        """Build the menu structure for the main window."""
        main_menu = self.menuBar()
        help_menu = main_menu.addMenu('H&elp')
        view_menu = main_menu.addMenu('Vi&ew')
        file_menu = main_menu.addMenu('R&ecent Files')
        edit_menu = main_menu.addMenu('&Edit')
        search_menu = main_menu.addMenu('S&earch')
        tools_menu = main_menu.addMenu('Sp&ecial Tools')

        # Help menu
        action_tip = QAction("Tip of th&e Day", self)
        action_tip.triggered.connect(self.show_tip)
        help_menu.addAction(action_tip)

        # View menu
        theme_menu = view_menu.addMenu("Th&emes")
        action_light_theme = QAction("Light mod&e", self)
        action_light_theme.triggered.connect(self.set_light_theme)
        theme_menu.addAction(action_light_theme)
        action_dark_theme = QAction("Dark mod&e", self)
        action_dark_theme.triggered.connect(self.set_dark_theme)
        theme_menu.addAction(action_dark_theme)
        accessibility_menu = view_menu.addMenu("Acc&essibility")
        action_hotdogstand_theme = QAction("High visibility th&eme", self)
        action_hotdogstand_theme.triggered.connect(self.set_hotdogstand_theme)
        accessibility_menu.addAction(action_hotdogstand_theme)
        action_quitedark_theme = QAction("Th&eme for blind users", self)
        action_quitedark_theme.triggered.connect(self.set_quitedark_theme)
        accessibility_menu.addAction(action_quitedark_theme)

        # Special Tools menu
        font_menu = QAction("Chang&e Font", self)
        font_menu.triggered.connect(self.change_font)
        tools_menu.addAction(font_menu)

        # Edit menu
        action_insert_symbol = QAction("Ins&ert symbol", self)
        action_insert_symbol.triggered.connect(self.insert_emoji)
        edit_menu.addAction(action_insert_symbol)

        # Search menu
        action_open = QAction("S&earch for file to open", self)
        action_open.triggered.connect(self.open_file)
        search_menu.addAction(action_open)
        action_save = QAction("S&earch for file to save", self)
        action_save.triggered.connect(self.save_file)
        search_menu.addAction(action_save)
        action_new = QAction("S&earch for a new file", self)
        action_new.triggered.connect(self.new_file)
        search_menu.addAction(action_new)

        # SubMenu Test
        testmenu = []
        for i in range(0, 200):
            testmenu.append(file_menu.addMenu(f'{i}'))

    def do_eula(self):
        """Display the End-User License Agreement and prompt the user to accept."""
        with open('crocpad\\EULA.txt', 'r', encoding='utf8') as f:
            eula = f.read()
        eula_dialog = EulaDialog(eula)
        eula_quiz_dialog = EulaQuizDialog()
        # run the EULA quiz, to make sure they read and understand
        while not eula_quiz_dialog.quiz_correct():
            eula_dialog.exec_()  # makes dialog modal (user cannot access main window)
            if eula_dialog.clicked_button == eula_dialog.eula_agree_button:
                # We click the agree button
                app_config['License']['eulaaccepted'] = 'yes'
                save_config(app_config)
            eula_quiz_dialog.exec_()

    def show_tip(self):
        """Randomly choose one tip of the day and display it."""
        with open('crocpad\\tips.txt', 'r', encoding='utf8') as f:
            tips = f.readlines()
        tip = random.choice(tips)
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Tip of the Day")
        dlg.setText(tip.strip())
        dlg.setIcon(QMessageBox.Information)
        dlg.show()

    def change_font(self):
        """Prompt the user for a font to change to."""
        # Do the users REEEEEALY need to change font :D
        font, ok = QFontDialog.getFont()
        if ok:
            print(font.toString())

    def eventFilter(self, source: QObject, event: QEvent) -> bool:
        """Override the eventFilter method of QObject to intercept keystrokes."""
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
            if event.key() == Qt.Key_Space:  # prank user with instant disappearing dialog
                if random.random() > 0.8:
                    dlg = QMessageBox(self)
                    dlg.setWindowTitle("Are you sure?")
                    dlg.setText("_" * 100)
                    dlg.show()
                    dlg.close()
        return False  # imitate overridden method

    def update_title(self):
        """Set title of main window with current file being edited."""
        self.setWindowTitle(f"Crocpad++ - {self.filename}")

    def edit_toggle_wrap(self):
        """Toggle the line wrap flag in the text editor."""
        self.text_window.setLineWrapMode(not self.text_window.lineWrapMode())

    def open_file(self):
        """Ask the user for a filename to open, and load it into the text editor.

        Called by the Open File menu action."""
        filename = QFileDialog.getOpenFileName()[0]
        with open(filename, 'r', encoding='utf-8') as file:
            self.text_window.setPlainText(file.read())
        self.filename = filename
        self.update_title()

    def save_file(self):
        """Ask the user for a filename to save to, and write out the text editor.

        Called by the Save File menu action."""
        filename = QFileDialog.getSaveFileName()[0]
        text = self.text_window.document().toPlainText()
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(text)
        self.filename = filename
        self.update_title()

    def new_file(self):
        """Clear the text editor and insert a helpful message.

        Called by the New File menu action."""
        self.filename = "** Untitled **"
        self.update_title()
        self.text_window.document().clear()
        self.text_window.insertPlainText("""To remove this message, please make sure you have entered
your full credit card details, made payable to:
Crocpad++ Inc
PO BOX 477362213321233
Cheshire Cheese
Snekland
Australia""")

    def set_light_theme(self):
        """Set the text view to the light theme."""
        self.app.setStyleSheet(crocpad.stylesheets.light)

    def set_dark_theme(self):
        """Set the text view to the dark theme."""
        self.app.setStyleSheet(crocpad.stylesheets.dark)

    def set_hotdogstand_theme(self):
        """Set the text view to the High Contrast theme."""
        self.app.setStyleSheet(crocpad.stylesheets.hotdogstand)

    def set_quitedark_theme(self):
        """Set the text view to the Quite Dark theme for the legally blind."""
        self.app.setStyleSheet(crocpad.stylesheets.quitedark)

    def insert_emoji(self):
        """Open a modal EmojiPicker dialog which can insert arbitrary symbols at the cursor."""
        picker = EmojiPicker(self.text_window.textCursor())
        picker.exec_()

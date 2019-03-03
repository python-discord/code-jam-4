import logging
import sys

from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QMainWindow, QApplication, \
    QHBoxLayout, QVBoxLayout, QWidget, QListWidgetItem

from project import ClipboardManager
from project.ClipboardManager.ClipboardObject import TextClipboardObject, ImageClipboardObject
from project.Plugins.Systray import SystemTrayIcon
from project.Stack import Stack
from project.Widgets import MainListWidget, TextListWidgetItem
from project.Widgets.MainListWidget import ImageListWidgetItem
from project.Widgets.SettingsScreen import SettingsScreen
from .utils import CONSTANTS


class ActionBar(QWidget):
    """ A bar which contains the controls for adding to this list of clipboard items"""

    def __init__(self):
        super().__init__()
        _horizontal_layout = QHBoxLayout(self)

        # self._add_btn = QtWidgets.QPushButton("Add")
        # can we not do this in the constructor?
        # self._add_btn.setObjectName(MainWindow.ADD_BUTTON_NAME)

        self._remove_btn = QtWidgets.QPushButton("Remove")
        # self._remove_btn.setGeometry(QtCore.QRect(50, 3, 51, 20))
        # self._remove_btn.clicked.connect()
        self._remove_btn.setObjectName(MainWindow.REMOVE_BUTTON_NAME)

        self._edit_btn = QtWidgets.QPushButton("Edit")
        # self._edit_btn.setGeometry(QtCore.QRect(100, 3, 51, 20))
        self._edit_btn.setObjectName(MainWindow.EDIT_BUTTON_NAME)

        self._move_up_btn = QtWidgets.QPushButton("Move Up")
        self._move_up_btn.setObjectName(MainWindow.MOVE_UP_BUTTON_NAME)

        self._move_down_btn = QtWidgets.QPushButton("Move Down")
        self._move_down_btn.setObjectName(MainWindow.MOVE_DOWN_BUTTON_NAME)

        # _horizontal_layout.addWidget(self._add_btn)
        _horizontal_layout.addWidget(self._remove_btn)
        _horizontal_layout.addWidget(self._edit_btn)
        _horizontal_layout.addWidget(self._move_up_btn)
        _horizontal_layout.addWidget(self._move_down_btn)

        _horizontal_layout.addStretch(1)


class MainWindow(QMainWindow):
    add_btn_signal = pyqtSignal()
    remove_btn_signal = pyqtSignal()

    move_up_btn_signal = pyqtSignal()
    move_down_btn_signal = pyqtSignal()

    item_selected = pyqtSignal(int)

    """ MainWindow """
    # strange constants:
    CENTRAL_WIDGET_NAME = 'central_widget'
    ADD_BUTTON_NAME = 'add_btn'
    REMOVE_BUTTON_NAME = 'remove_btn'
    EDIT_BUTTON_NAME = 'edit_btn'
    MOVE_UP_BUTTON_NAME = 'move_up_btn'
    MOVE_DOWN_BUTTON_NAME = 'move_down_btn'

    # please label what these are / relate to:
    num_of_objects = 0
    items = []

    def __init__(self, clipboard_manager: ClipboardManager):
        """ Initialises new MainWindow class """
        super().__init__()
        self._logger = logging.getLogger(self.__class__.__qualname__)

        self._central_widget_layout = QVBoxLayout()
        self._central_widget = QtWidgets.QWidget(self)
        self._clipboard_manager = clipboard_mgr

        # self._clipboard_manager.bind_clipboard_state_callback(self._render_clipboard_stack)
        self._clipboard_manager.clipboard_changed_signal.connect(self._render_clipboard_stack)
        self._clipboard_manager.stack_changed_signal.connect(self._render_clipboard_stack)

        self.remove_btn_signal.connect(self._clipboard_manager.remove_clipboard_item)
        self.move_up_btn_signal.connect(self._clipboard_manager.move_selected_item_up)
        self.move_down_btn_signal.connect(self._clipboard_manager.move_selected_item_down)

        self.item_selected.connect(self._clipboard_manager.set_selected_object)
        # self._main_list_widget.itemClicked.connect(self._set_selected_object)

        self._settings_screen = SettingsScreen(self)

        self._init_ui()

    @pyqtSlot(int)
    def _set_current_row(self, idx):
        # if no item is selected, idx will be -1
        if idx > -1:
            self.item_selected.emit(self._clipboard_manager
                                    .clipboard_stack.items_count() - max(0, idx) - 1)

    # @pyqtSlot(QListWidgetItem)
    # def _set_selected_object(self, list_item: QListWidgetItem):
    #     self.item_selected.emit(self._main_list_widget.currentRow())

    def _init_ui(self):
        self.setWindowTitle(CONSTANTS['NAME'])
        # self.setGeometry(self.left, self.top, self.width, self.height)
        self.setupUi()
        self.show()

    def _show_settings_window(self):
        self._settings_screen.show()

    def _show_plugins_window(self):
        pass

    @pyqtSlot(Stack)
    def _render_clipboard_stack(self, clipboard_stack: Stack):
        self._main_list_widget.clear()
        # newest items should be at the top
        for (idx, clipboard_object) in enumerate(reversed(clipboard_stack.items())):
            if isinstance(clipboard_object, TextClipboardObject):
                _item = QListWidgetItem(self._main_list_widget)
                _custom_item = TextListWidgetItem(clipboard_stack.items_count()
                                                  - idx - 1, clipboard_object)
                _item.setSizeHint(_custom_item.sizeHint())

                self._main_list_widget.addItem(_item)
                self._main_list_widget.setItemWidget(_item, _custom_item)

            elif isinstance(clipboard_object, ImageClipboardObject):
                _item = QListWidgetItem(self._main_list_widget)
                _custom_item = ImageListWidgetItem(clipboard_stack.items_count() - idx - 1,
                                                   clipboard_object)
                _item.setSizeHint(_custom_item.sizeHint())
                self._main_list_widget.addItem(_item)
                self._main_list_widget.setItemWidget(_item, _custom_item)

        self._main_list_widget.setCurrentRow(self._clipboard_manager.clipboard_stack.items_count()
                                             - self._clipboard_manager.clipboard_stack
                                             .current_item_idx - 1)

    def setupUi(self):

        self._central_widget.setObjectName(MainWindow.CENTRAL_WIDGET_NAME)

        self._action_bar = ActionBar()
        self._action_bar._remove_btn.clicked.connect(self.remove_btn_signal)
        self._action_bar._move_up_btn.clicked.connect(self.move_up_btn_signal)
        self._action_bar._move_down_btn.clicked.connect(self.move_down_btn_signal)

        self._central_widget_layout.addWidget(self._action_bar)

        self._main_list_widget = MainListWidget()
        self._main_list_widget.currentRowChanged.connect(self._set_current_row)

        self._central_widget_layout.addWidget(self._main_list_widget)

        self.menubar = self.menuBar()
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuFile.setTitle("Settings")

        self.actionSettings = QtWidgets.QAction(self)
        self.actionSettings.setObjectName("actionSettings")
        self.actionSettings.setText("General")
        self.actionSettings.triggered.connect(self._show_settings_window)

        self.menuFile.addAction(self.actionSettings)

        self.pluginSettings = QtWidgets.QAction(self)
        self.pluginSettings.setObjectName("actionPlugins")
        self.pluginSettings.setText('Plugins')
        self.pluginSettings.triggered.connect(self._show_plugins_window)

        self.menuFile.addAction(self.pluginSettings)

        self.menubar.addAction(self.menuFile.menuAction())

        self._central_widget.setLayout(self._central_widget_layout)
        self.setCentralWidget(self._central_widget)

        # https://stackoverflow.com/questions/2462401/problem-in-understanding-connectslotsbyname-in-pyqt
        # Better to use new-style decorator @QtCore.pyqtSlot()
        # QtCore.QMetaObject.connectSlotsByName(self)

        self.show()

    def keyPressEvent(self, event):
        self._logger.info("Key press detected")
        if event.matches(QKeySequence.Paste):
            self._logger.info("Detected paste")

    def closeEvent(self, event):
        """ Fires on window close"""
        pass


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info("App Started")
    app = QApplication(sys.argv)

    app.setWindowIcon(QIcon("./project/icon.ico"))

    clipboard_mgr = ClipboardManager.ClipboardManager()
    main_window = MainWindow(clipboard_mgr)

    # Creates and starts systray icon
    w = QtWidgets.QDesktopWidget()
    systray = SystemTrayIcon(w)
    systray.show()

    sys.exit(app.exec_())

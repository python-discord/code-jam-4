from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QCheckBox, QHBoxLayout, QPushButton

from project.ConfigManager import ConfigManager


class SettingsScreen(QMainWindow):

    def _persist_clipboard_checkbox_clicked(self):
        _config_mgr = ConfigManager.get_instance()
        _config_mgr.persist_clipboard = not _config_mgr.persist_clipboard
        self._dirty = True
        self._save_btn.setDisabled(False)

    def _delete_after_paste_checkbox_clicked(self):
        _config_mgr = ConfigManager.get_instance()
        _config_mgr.delete_after_paste = not _config_mgr.delete_after_paste
        print(_config_mgr.delete_after_paste)
        self._dirty = True
        self._save_btn.setDisabled(False)

    def _auto_load_top_checkbox_clicked(self):
        _config_mgr = ConfigManager.get_instance()
        _config_mgr.auto_load_top = not _config_mgr.auto_load_top
        self._dirty = True
        self._save_btn.setDisabled(False)

    def _save_clicked(self):
        _config_mgr = ConfigManager.get_instance()
        _config_mgr.save()
        self._dirty = False
        self._save_btn.setDisabled(True)

    def __init__(self, parent=None):
        super(SettingsScreen, self).__init__(parent)
        self.setWindowTitle("Settings")
        _config_mgr = ConfigManager.get_instance()

        self._dirty = False  # Changed settings but not saved

        self._central_widget_layout = QVBoxLayout()
        self._central_widget = QWidget(self)

        # Checkboxes begin here
        self._persist_clipboard_checkbox = QCheckBox("Persist clipboard upon app quit", self)
        self._delete_after_paste_checkbox = QCheckBox("Delete selected clipboard item after paste", self)
        self._auto_load_top_checkbox = QCheckBox("Automatically load top item into clipboard", self)

        self._persist_clipboard_checkbox.setChecked(_config_mgr.persist_clipboard)
        self._delete_after_paste_checkbox.setChecked(_config_mgr.delete_after_paste)
        self._auto_load_top_checkbox.setChecked(_config_mgr.auto_load_top)

        self._persist_clipboard_checkbox.toggled.connect(self._persist_clipboard_checkbox_clicked)
        self._delete_after_paste_checkbox.toggled.connect(self._delete_after_paste_checkbox_clicked)
        self._auto_load_top_checkbox.toggled.connect(self._auto_load_top_checkbox_clicked)

        self._central_widget_layout.addWidget(self._persist_clipboard_checkbox)
        self._central_widget_layout.addWidget(self._delete_after_paste_checkbox)
        self._central_widget_layout.addWidget(self._auto_load_top_checkbox)

        # Bottom save button
        self._bottom_save_widget = QWidget()
        self._bottom_save_layout = QHBoxLayout()
        self._bottom_save_layout.addStretch(1)
        self._save_btn = QPushButton("Save")
        self._save_btn.clicked.connect(self._save_clicked)
        self._bottom_save_layout.addWidget(self._save_btn)

        self._bottom_save_widget.setLayout(self._bottom_save_layout)
        self._central_widget_layout.addWidget(self._bottom_save_widget)

        self._central_widget.setLayout(self._central_widget_layout)
        self.setCentralWidget(self._central_widget)

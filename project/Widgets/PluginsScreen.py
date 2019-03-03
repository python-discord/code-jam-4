import logging

from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, \
    QGroupBox, QCheckBox, QHBoxLayout, QPushButton, QLabel

from project.ConfigManager import ConfigManager
from project.PluginManager import PluginManager


class PluginsScreen(QMainWindow):
    """Enable and disable some of our enhancers"""

    def _save_clicked(self):
        _config_mgr = ConfigManager.get_instance()
        _config_mgr.save()
        self._dirty = False
        self._save_btn.setDisabled(True)

    def _text_plugin_checkbox_clicked(self, checked, name):
        self._dirty = True
        self._save_btn.setDisabled(False)
        # self._logger.info(name + ': ' + str(checked))
        _config_mgr = ConfigManager.get_instance()
        if checked:
            _config_mgr.enable_text_plugin(name)
        else:
            _config_mgr.disable_text_plugin(name)

    def _image_plugin_checkbox_clicked(self, checked, name):
        self._dirty = True
        self._save_btn.setDisabled(False)
        _config_mgr = ConfigManager.get_instance()
        if checked:
            _config_mgr.enable_image_plugin(name)
        else:
            _config_mgr.disable_image_plugin(name)

    def __init__(self, parent=None):
        super().__init__(parent)

        self._logger = logging.getLogger(self.__class__.__qualname__)

        self._plugin_manager = PluginManager.get_instance()

        self.setWindowTitle("Plugins")

        _config = ConfigManager.get_instance()
        self._dirty = False

        self._central_widget_layout = QVBoxLayout()
        self._central_widget = QWidget(self)

        self._text_plugins_group_box = QGroupBox("Text Enhancers")
        self._image_plugins_group_box = QGroupBox("Image Enhancers")

        _vbox1 = QVBoxLayout()

        for plugin in self._plugin_manager.text_plugins:

            _checkbox = QCheckBox(plugin.__class__.name(), self)

            if plugin.__class__.name() not in _config.disabled_text_plugins:
                _checkbox.setChecked(True)

            # https://stackoverflow.com/questions/19837486/python-lambda-in-a-loop
            _checkbox.toggled.connect(lambda checked, name=plugin.__class__.name():
                                      self._text_plugin_checkbox_clicked(checked, name))

            _vbox1.addWidget(_checkbox)
            _vbox1.addWidget(QLabel(plugin.__class__.description()))

        self._text_plugins_group_box.setLayout(_vbox1)

        _vbox2 = QVBoxLayout()

        for plugin in self._plugin_manager.image_plugins:
            _checkbox = QCheckBox(plugin.__class__.name(), self)

            if plugin.__class__.name() not in _config.disabled_image_plugins:
                _checkbox.setChecked(True)

            _checkbox.toggled.connect(lambda checked, name=plugin.__class__.name():
                                      self._image_plugin_checkbox_clicked(checked, name))

            _vbox2.addWidget(_checkbox)
            _vbox2.addWidget(QLabel(plugin.__class__.description()))

        self._image_plugins_group_box.setLayout(_vbox2)

        self._central_widget_layout.addWidget(self._text_plugins_group_box)
        self._central_widget_layout.addWidget(self._image_plugins_group_box)

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

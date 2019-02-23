"""
.. module:: MainListView
    :synopsis: The scrollable area in the main user interface, \
    with helper functions to add or remove objects

.. moduleauthor:: TBD
"""
from PyQt5.QtWidgets import QListWidget


class MainListWidget(QListWidget):
    def __init__(self):
        super().__init__()
        self.addItem("Sample Item")

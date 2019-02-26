from typing import Any


class Clipboard:
    """
    This class represents an individual clipboard, to be used for cutting,
    copying and pasting data.

    TODO: Unused at the moment but might come in handy later for intercepting
          cuts, copies and pastes.
    """

    # instance = None
    #
    # def __new__(cls, *args, **kwargs):
    #     if not Clipboard.instance:
    #         Clipboard.instance = super().__new__(cls, *args, **kwargs)
    #     return Clipboard.instance

    def __init__(self):
        self.data = None

    def set_data(self, value):
        """
        Sets the data contained in this clipboard.

        :param value: The data to place in the clipboard.
        """
        self.data = value

    def get_data(self) -> Any:
        """
        Retrieve the data in this clipboard.

        :return: The data in this clipboard.
        """
        return self.data


# A shared instance of Clipboard that can be imported across different modules.
shared_clipboard = Clipboard()

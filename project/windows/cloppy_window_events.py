from project.functionality.events import Event


class CloppyChoiceMadeEvent(Event):
    """
    This class represent an event emitter for cloppy choice events.
    These are emitted every time input is received from the user in order to
    make a choice in a CloppyWindow.

    It passes data to its callbacks using a CloppyChoiceMadeEventData object.
    These will contain information about the question asked and the choice
    made by the user in response.
    """
    def __call__(self, message, choice):
        super().__call__(
            CloppyChoiceMadeEventData(message, choice)
        )


class CloppyChoiceMadeEventData:
    """
    This class is used to propagate information about a choice a user has made
    to callbacks registered in a CloppyChoiceMadeEvent object.
    """
    def __init__(self, message, choice):
        self.message = message
        self.choice = choice

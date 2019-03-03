from project.functionality.events import Event


class NewWordEvent(Event):
    """
    This class represent an event emitter for new word events.
    These are emitted every time the user is detected to have typed a word.

    It passes data to its callbacks using a NewWordEventData object.
    These will contain information about the word's contents, and its
    starting and ending indexes.
    """

    def __call__(self, start, end, word):
        super().__call__(
            NewWordEventData(start, end, word)
        )


class NewWordEventData:
    """
    This class is used to propagate information about a word a user has typed
    to callbacks registered in a NewWordEvent object.
    """
    def __init__(self, start, end, word):
        self.start = start
        self.end = end
        self.word = word

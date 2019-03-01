from project.functionality.events import Event


class CloppyChoiceMadeEvent(Event):
    def __call__(self, message, choice):
        super().__call__(
            CloppyChoiceMadeEventData(message, choice)
        )


class CloppyChoiceMadeEventData:
    def __init__(self, message, choice):
        self.message = message
        self.choice = choice

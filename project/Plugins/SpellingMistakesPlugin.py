import string
from random import randint, choice

from project import Stack
from project.ClipboardManager.ClipboardObject import TextClipboardObject
from project.Plugins import AbstractPlugin


def _random_spelling_mistakes(text):
    text = text.split()
    new_words = ''
    for word in text:
        if len(word) == 1 or len(word) == 2:
            final = ''.join(word)
            new_words = new_words + ' ' + final
        else:
            spot = randint(0, len(word) - 1)
            if spot == 0:
                '''Give it two chances to not be 0, I think its better
                if its mostly the middle letters that get removed'''
                spot = randint(0, len(word) - 1)
                if spot == 0:
                    pass
            final = ''.join(word)
            final = final[0:spot] + choice(string.ascii_letters) + final[spot:]
            new_words = new_words + ' ' + final
    return new_words


class SpellingMistakesPlugin(AbstractPlugin):

    @staticmethod
    def name() -> str:
        return "SpellingMistakes"

    @staticmethod
    def description() -> str:
        return "To help you sound more natural when writing."

    def onload(self):
        pass

    def unload(self):
        pass

    def on_copy(self, copied_input: any, stack: Stack):
        self._logger.debug(SpellingMistakesPlugin.name() + " called: " + copied_input)
        # stack.push_item(copied_input)
        stack.push_item(TextClipboardObject(_random_spelling_mistakes(copied_input)))
        self._logger.info("Stack size" + str(stack.items_count()))

    def on_paste(self, stack: Stack):
        return stack

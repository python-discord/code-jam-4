from random import randint

import thesaurus

from project import Stack
from project.ClipboardManager.ClipboardObject import TextClipboardObject
from project.Plugins import AbstractPlugin


def _synonym(text):
    skip_word = False
    text = text.split()
    new_words = ''
    for word in text:
        if skip_word:
            new_words = new_words + ' ' + word
            skip_word = False
        else:
            skip_word = True
            try:
                w = thesaurus.Word(word)
                w.synonyms('all')
                text = w.synonyms()[randint(0, len(w))]
                final = ''.join(text)
                new_words = new_words + ' ' + final
            except thesaurus.exceptions.MisspellingError:
                new_words = new_words + ' ' + word
            except thesaurus.exceptions.WordNotFoundError:
                new_words = new_words + ' ' + word
            except TypeError:
                new_words = new_words + ' ' + word
    return new_words


class SynonymPlugin(AbstractPlugin):

    def onload(self):
        pass

    def unload(self):
        pass

    def on_copy(self, copied_input: any, stack: Stack):
        stack.push_item(TextClipboardObject(_synonym(copied_input)))
        self._logger.info("Stack size" + str(stack.items_count()))

    def on_paste(self, stack: Stack):
        return stack

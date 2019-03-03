import time
from random import randint

import thesaurus

from project import Stack
from project.ClipboardManager.ClipboardObject import TextClipboardObject
from project.Plugins import AbstractPlugin


class SynonymPlugin(AbstractPlugin):

    def _synonym(self, text):
        skip_word = False
        start = time.time()
        text = text.split()
        new_words = ''
        for word in text:
            if skip_word:
                new_words = new_words + ' ' + word
                skip_word = False
            else:
                # start_ = time.time()
                skip_word = True
                try:
                    w = thesaurus.Word(word)
                    w.synonyms('all')
                    _synonyms = w.synonyms()
                    text = _synonyms[randint(0, len(_synonyms) - 1)]
                    final = ''.join(text)
                    new_words = new_words + ' ' + final
                except thesaurus.exceptions.MisspellingError:
                    new_words = new_words + ' ' + word
                except thesaurus.exceptions.WordNotFoundError:
                    new_words = new_words + ' ' + word
                except TypeError:
                    new_words = new_words + ' ' + word
                # end_ = time.time()
        end = time.time()
        self._logger.info('processing time: ' + str(end - start))
        return new_words

    @staticmethod
    def name() -> str:
        return "Synonyms"

    @staticmethod
    def description() -> str:
        return "Picks up the thesaurus for you so you don't have to."

    def onload(self):
        pass

    def unload(self):
        pass

    def on_copy(self, copied_input: any, stack: Stack):
        stack.push_item(TextClipboardObject(self._synonym(copied_input)))
        self._logger.info("Stack size" + str(stack.items_count()))

    def on_paste(self, stack: Stack):
        return stack

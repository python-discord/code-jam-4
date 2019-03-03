import tkinter as tk

from project.spelling.correction import is_correct
from project.spelling.misspell import misspell


class SpellingWindow(tk.Toplevel):
    def __init__(self, master, word):
        super().__init__(master)
        self.word = word

    def can_misspell(self):
        # If the word is correct already, we can't correct
        # it further
        if is_correct(self.word):
            return False

        # If a word can't be misspelled, when we call `misspell()`
        # on it, the result will be the same as the word.
        return self.word != misspell(self.word)

    def misspellings(self):
        result = []

        while len(result) < 4:
            misspelling = misspell(self.word)

            if misspelling not in result:
                result.append(misspelling)

        return result

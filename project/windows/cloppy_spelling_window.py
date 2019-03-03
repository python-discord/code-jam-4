import random

from project.windows.cloppy_window import CloppyButtonWindow
from project.windows.cloppy_window_events import CloppyChoiceMadeEventData

from project.windows.editor_window_events import NewWordEventData

from project.spelling.correction import correction
from project.spelling.misspell import misspell


class CloppySpellingWindow(CloppyButtonWindow):
    """
    This class represents individual Cloppy windows used to suggest spelling
    corrections to the user.
    """
    def __init__(self, master, word_data: NewWordEventData):
        super().__init__(master)

        self.word = word_data.word.lower()
        self.start = word_data.start
        self.end = word_data.end

        self.set_message(
            f"Looks like the word '{word_data.word}' could be a "
            "misspelling.\n"
            "Below are some suggested corrections.\n"
            "If you don't pick one within 10 seconds I'll pick one for you,\n"
            "to save you time. :)"
        )

        corrected_word = correction(self.word)

        self.suggestions = [corrected_word]

        for i in range(3):
            suggestion = misspell(corrected_word, 3)
            if suggestion and suggestion not in self.suggestions:
                self.suggestions.append(suggestion)

        for suggestion in random.sample(
            self.suggestions, len(self.suggestions)
        ):
            self.add_choice(suggestion)

        self.set_time_limit(10)
        self.choice_made.add_callback(self.replace_word)

    def replace_word(self, choice_data: CloppyChoiceMadeEventData):
        self.master.set_text(
            choice_data.choice, self.start, self.end
        )

    def time_out(self):
        self.make_choice(random.choice(self.suggestions))

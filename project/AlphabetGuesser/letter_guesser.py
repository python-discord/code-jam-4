import pickle


class LetterGuesser:
    """
    LetterGuesser:

    === Public Attributes ===
    dictionary
    possible_characters

    === Methods ===
    request_question: returns a question that can be printed to the user
    remove_possible_letters: removes all characters from possible_characters that are contained in the given word/phrase
    remove_possible_words: removes all words/phrases from dictionary that contain the exact same characters as the given
                           word/phrase
    contains_all_letters: Returns True only if all the letters in word_2 are contained in word_1
    """
    def __init__(self):
        self.dictionary = None
        self.possible_characters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q',
                                    'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7',
                                    '8', '9', '@', '.', '-', ' ', '?', '!']
        with open("words_pickle", "rb") as openfile:
            self.dictionary = pickle.load(openfile)
            openfile.close()

        # Test word, this assumes that the user said that this word doesn't contain any of the letters they want
        self.remove_possible_words('qweoiuirwpeoitulkjashdflghmnbzxcv')

    def request_question(self) -> str:
        pass

    def remove_possible_letters(self, word) -> None:
        pass

    def remove_possible_words(self, word) -> None:
        words_to_delete = []
        for elem in self.dictionary:
            if self.contains_all_letters(word, elem):
                print('{0} contains all the letters in {1}'.format(word, elem))
                words_to_delete.append(elem)
        for elem in words_to_delete:
            del self.dictionary[elem]

    @staticmethod
    def contains_all_letters(word_1, word_2) -> bool:
        for letter in word_2:
            if letter not in word_1:
                return False
        return True


if __name__ == '__main__':
    guesser = LetterGuesser()

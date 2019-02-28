import pickle
import random


class LetterGuesser:
    """
    LetterGuesser:

    === Public Attributes ===
    dictionary
    possible_characters

    === Methods ===
    request_word: returns a random word from the dictionary
    remove_possible_letters: removes all characters from possible_characters that are not contained in the given
                             word/phrase
    remove_possible_words: removes all words/phrases from dictionary that contain none of the characters in the given
                           word/phrase
    contains_none_letters: Returns True only if none the letters in word_2 are contained in word_1
    answer: Handles the user's answer of either "Yes" or "No"
    """
    def __init__(self):
        self.dictionary = None
        self.possible_characters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q',
                                    'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7',
                                    '8', '9', '@', '.', '-', ' ', '?', '!']
        with open("words_pickle", "rb") as openfile:
            self.dictionary = pickle.load(openfile)
            openfile.close()

    def answer(self, requested_word, answer):
        """
        Handles the user's answer for a given word
        :param requested_word: The context of the user's answer
        :param answer: string that should be either "Yes" or "No"; the program will  not respond to anything else
        :return: None
        """
        if answer == "Yes":
            self.remove_possible_words(requested_word)
        self.remove_possible_letters(requested_word, answer)

    def request_word(self) -> str:
        return random.choice(list(self.dictionary))

    def remove_possible_letters(self, word, yes_no) -> None:
        characters_to_delete = []
        for character in self.possible_characters:
            if character not in word and yes_no == "Yes":
                characters_to_delete.append(character)
            elif character in word and yes_no == "No":
                characters_to_delete.append(character)
        for character in characters_to_delete:
            self.possible_characters.remove(character)

    def remove_possible_words(self, word) -> None:
        words_to_delete = []
        for elem in self.dictionary:
            if self.contains_none_letters(elem, word):
                words_to_delete.append(elem)
        for elem in words_to_delete:
            del self.dictionary[elem]

    @staticmethod
    def contains_none_letters(word_1, word_2) -> bool:
        for letter in word_1:
            if letter in word_2:
                return False
        return True


if __name__ == '__main__':
    """
    This is a simple demo showing how the letter guesser should be implemented
    """
    guesser = LetterGuesser()
    print('Pick a letter, any letter; keep it in mind as you answer these questions!\n')
    while True:
        word = guesser.request_word()
        yes_no = input('Is your letter in the word/phrase:\n{}\n(Yes/No):'.format(word))
        guesser.answer(word, yes_no)
        print(guesser.possible_characters)
        if len(guesser.possible_characters) == 1:
            print('The letter you want is \'{0}\''.format(guesser.possible_characters[0]))
            break
        if len(guesser.possible_characters) < 1:
            print('A mistake has been made; try again')
            break

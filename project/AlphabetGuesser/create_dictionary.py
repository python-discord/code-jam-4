import pickle


def create_dictionary() -> None:
    """
    Reads each word from a file with the format of words.txt & determines what letters comprise each
        word; saved into a dictionary in the following format:
        {'apple': [a, e, l, p], 'banana': [a, b, n], ...etc}
        Finally, the created dictionary is saved as a pickle
    :return: None
    """
    dictionary = {}
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q',
                'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7',
                '8', '9', '@', '.', '-', ' ', '?', '!']
    with open('words.txt') as f:
        for word in f:
            word = word[:len(word) - 1]
            letters = []
            for letter in alphabet:
                if letter in word:
                    letters.append(letter)
            dictionary[word] = letters
        f.close()
    with open("words_pickle", 'wb') as outfile:
        pickle.dump(dictionary, outfile)


if __name__ == '__main__':
    create_dictionary()

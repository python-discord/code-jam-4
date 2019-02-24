from random import randint, choice
import string


def random_spelling_mistakes(text):
    '''
    Usage: Will add random letters to words (only words above 2 letters)
    then return the new sentence.

    Example:

    print(random_spelling_mistakes('Hello, yes hi'))

    Heqllo, yeVs hi
    '''

    # TODO: make it the same case as word changing, looks better
    text = text.split()
    new_words = ''
    print(text)
    for word in text:
        if len(word) == 1 or len(word) == 2:
            final = ''.join(word)
            new_words = new_words + ' ' + final
        else:
            spot = randint(0, len(word) - 1)
            if spot == 0:
                '''Give it two chances to not be 0, I think its better if its mostly the middle letters that get 
                removed'''
                spot = randint(0, len(word) - 1)
                if spot == 0:
                    pass
            final = ''.join(word)
            final = final[0:spot] + choice(string.ascii_letters) + final[spot:]
            new_words = new_words + ' ' + final
    return new_words
    # TODO: there is a '.\PredictiveText.py:28:97: W291 trailing whitespace' and i cant resolve

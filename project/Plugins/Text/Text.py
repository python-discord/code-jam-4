import string
from random import randint, choice
import requests
from lxml import html
import thesaurus
import time


def apply(text):
    """Use this function, not any other one. It as a 50/50 chance of applying each"""

    text = synonym(text)
    return text

    # if randint(0, 1):
    #     text = synonym(text)
    #     return text
    # else:
    #     text = quotify(text)
    #     return text


def random_spelling_mistakes(text):
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


def quotify(text):
    try:
        page = requests.get('https://funnysentences.com/sentence-generator/')
        tree = html.fromstring(page.content)
        quote = tree.xpath('//*[@id="sentencegen"]/text()')
        return ''.join(quote)
    except requests.exceptions.ConnectionError:
        return "lol you don't have internet"


def synonym(text):
    start = time.time()

    #if len(text) >
    print('Processing...')
    text = text.split()
    new_words = ''
    for word in text:
        print("Processing Word '", word, "'")
        try:
            w = thesaurus.Word(word)
            w.synonyms('all')
            text = w.synonyms()[randint(0, len(w))]
            final = ''.join(text)
            new_words = new_words + ' ' + final
        except thesaurus.exceptions.MisspellingError:
            print("Error. Skipping word: ' ", word, " '")
            new_words = new_words + ' ' + word
            new_words = new_words + ' ' + word
        except thesaurus.exceptions.WordNotFoundError:
            print("Error. Skipping word: ' ", word, " '")
            new_words = new_words + ' ' + word
            new_words = new_words + ' ' + word
        except TypeError:
            print("Error. Skipping word: ' ", word, " '")
            new_words = new_words + ' ' + word
            new_words = new_words + ' ' + word
    end = time.time()
    print(end - start)
    return new_words

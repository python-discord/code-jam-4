from random import randint, choice
import string
import json

def __init__():
    from project.Plugins.Save import getQuotes

    # Quotes are now loadeded from 'app.json' instead of being hard coded
    quotes = getQuotes()


class Vars:
    times_appled = 0


'''Use this function, not any other one. It as a 50/50 chance of applying each'''


def apply(text):
    """First time coping, its normal, then it starts to go down hill...."""
    Vars.times_appled = + 1
    if Vars.times_appled > 0 and Vars.times_appled < 2:
        if randint(0, 5) == 5:
            text = random_spelling_mistakes(text)
            return text
        else:
            return text
    elif Vars.times_appled > 2 and Vars.times_appled < 4:
        if randint(0, 5) == 5:
            text = random_spelling_mistakes(text)
            return text
        else:
            text = quotify(text)
            return text
    elif Vars.times_appled > 4 and Vars.times_appled < 15:
        if randint(0, 1) == 3:
            text = random_spelling_mistakes(text)
            return text
        else:
            text = quotify(text)
            return text

    elif Vars.times_appled > 15:
        text = quotify(text)
        return text
    else:
        return text


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
    from project.Plugins.Text import Parse
    quote = Parse.parse()
    return quote

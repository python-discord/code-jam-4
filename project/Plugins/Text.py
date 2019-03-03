from random import randint, choice
import string

quotes = [
    'O-oooooooooo AAAAE-A-A-I-A-U- JO-oooooooooooo AAE-O-A-A-U-U-A- E-eee-ee-eee AAAAE-A-E-I-E-A-JO-ooo-oo-oo-oo',
    '╠═══╣Lets build a ladder╠═══╣',
    '( ͠° ͟ʖ ͡°) OVERCONFIDENCE IS A SLOW AND INSIDIOUS KILLER ( ͠° ͟ʖ ͡°)',
    '┴┬┴┤( ͡° ͜ʖ├┬┴┬ HEY KIDS DO YOU WANT SOME DANK MEMES?',
    "(▀̿Ĺ̯▀̿ ̿) This is the 0-3 Police, You're coming with us. (▀̿Ĺ̯▀̿ ̿)",
    'Born too late to explore the Earth, born too early to explore the universe, born perfectly to explore dank memes',
    'Hi, my name is Bill Gates and today I’ll teach you how to count to ten: 1, 2, 3, 95, 98, NT, 2000, XP, Vista, 7,\
    8, 10',
]

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
                '''Give it two chances to not be 0, I think its better if its mostly the middle letters that get 
                removed'''
                spot = randint(0, len(word) - 1)
                if spot == 0:
                    pass
            final = ''.join(word)
            final = final[0:spot] + choice(string.ascii_letters) + final[spot:]
            new_words = new_words + ' ' + final
    return new_words


def quotify(text):
    try:
        text = quotes[randint(0, len(quotes))]
    except IndexError:
        try:
            text = quotes[randint(0, len(quotes))]
        except IndexError:
            print("Error: (IndexError) in PredictiveText.py. Try'ed to quotify but failed")
            return text
    finally:
        return text

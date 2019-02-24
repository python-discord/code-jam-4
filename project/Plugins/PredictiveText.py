# Not done yet, feel free to change it :p
from random import randint


class PredictiveText():

    def _random_spelling_mistakes(text):
        text = text.split()
        print(text)
        for word in text:
            length = len(word)
            if length == 1:
                return
            spot = randint(0, length - 1)

        return text

PredictiveText._random_spelling_mistakes('yelp hello I me')
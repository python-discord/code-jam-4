import project.spelling.consonants as consonants
import project.spelling.data as data

import math
import random
import re


arpabet = data.arpabet()


class Grapheme:
    def __init__(self, letters, phoneme=None):
        self.letters = letters
        self.phoneme = phoneme

    def __str__(self):
        return f"<Grapheme '{self.phoneme}' using letters '{self.letters}'>"


def phonemes(word):
    final = ",".join(arpabet[word][0])

    final = final.replace("K,S", "KS")
    final = final.replace("K,W", "KW")

    return final.split(",")


def find_grapheme(letters, phoneme):
    """
    Given letters, returns the first match of a phoneme,
    as well as any "junk" that's behind it.
    """
    for i in range(1, len(letters) + 1):
        substring = letters[:i]

        for grapheme in consonants.search[phoneme]:
            if grapheme in substring:
                extra = substring[:len(substring) - len(grapheme)]
                return Grapheme(extra), Grapheme(grapheme, phoneme)


def find_vowels(grapheme):
    letters = grapheme.letters
    regex = re.compile(".*?([aeioruy]+)$")
    result = regex.match(letters)

    if result is None:
        return grapheme, None
    else:
        vowels = result.group(1)
        carry = letters[:len(letters) - len(vowels)]
        return Grapheme(carry), Grapheme(vowels)


def find_consonant(letters, phoneme):
    for i in range(len(letters) + 1, 1, -1):
        substring = letters[:i]

        if substring in consonants.search[phoneme]:
            return substring


def graphemes(word):
    """
    Converts a word into its *graphemes* - i.e. separating
    the words into letters, with each chunk of letters representing
    either a consonant, a vowel or a vowel cluster.
    """
    final = []
    word_phonemes = phonemes(word)

    # Iterate over every phoneme in a word
    for phoneme in word_phonemes:
        # If that phoneme is a consonant:
        if phoneme in consonants.search.keys():
            # Find the first grapheme that matches that phoneme,
            # and include the extra letters behind it
            extra, grapheme = find_grapheme(word, phoneme)

            crop_length = 0

            # Algorithm to "carry" silent/vowels to consonants to last consonant,
            # since the consonant algorithm is lazy and gets the shortest
            # string possible
            if len(final) > 0:
                consonant = final[-1]

                # Creating a "letter pool" of possible characters that could
                # be in the previous vowel
                letter_pool = consonant.letters + extra.letters
                new_consonant = find_consonant(letter_pool, consonant.phoneme)

                # If we *do* find a new consonant:
                if new_consonant is not None:
                    # The amount of letters copied over from the extra letters
                    # to the new consonant
                    letters_from_extra = len(new_consonant) - len(consonant.letters)
                    # We need to delete more letters from "word" since we're editing
                    # "extra", so add those letters back again
                    crop_length += letters_from_extra
                    # Delete carried letters from "extra"
                    extra.letters = extra.letters[letters_from_extra:]
                    # Add the carried letters to the previous consonant
                    consonant.letters = new_consonant

            # If there are still any letters left in the "extra letters",
            # add it to the end as a vowel cluster
            if extra.letters != "":
                final.append(extra)

            final.append(grapheme)
            crop_length += len(extra.letters) + len(grapheme.letters)
            # Crop the word since we've already processed some letters
            word = word[crop_length:]
        else:
            continue

    # The last iteration of "carrying"
    if len(final) > 0:
        consonant = final[-1]

        letter_pool = consonant.letters + word
        new_consonant = find_consonant(letter_pool, consonant.phoneme)

        if new_consonant is not None:
            letters_from_word = len(new_consonant) - len(consonant.letters)
            word = word[letters_from_word:]
            consonant.letters = new_consonant

    if word != "":
        final.append(Grapheme(word))

    return final


def random_consonant(counter):
    total = sum(counter.values())
    random_value = math.floor(random.random() * total)
    current = 0

    for key, value in counter.items():
        if random_value <= current:
            return key

        current += value


def misspell(word):
    """
    Given a word, roughly misspell it.
    :param word:
    :return:
    """
    final_word = ""
    word_graphemes = graphemes(word)
    misspelling = int(random.random() * len([x for x in word_graphemes if x.phoneme]))
    current_consonant = 0

    for i in range(len(word_graphemes)):
        grapheme = word_graphemes[i]

        # Vowel cluster
        if grapheme.phoneme is None:
            final_word += grapheme.letters
        # Consonant
        else:
            if misspelling != current_consonant:
                final_word += grapheme.letters
                current_consonant += 1
                continue

            if i == 0:
                possible = consonants.replace_start[grapheme.phoneme]
            elif i == len(word_graphemes) - 1:
                possible = consonants.replace_end[grapheme.phoneme]
            else:
                possible = consonants.replace_middle[grapheme.phoneme]

            del possible[grapheme.letters]
            final_word += random_consonant(possible)

            current_consonant += 1

    return final_word

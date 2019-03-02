import random

import project.spelling
import re


arpabet = project.spelling.arpabet()

consonants = {
    "M": ["m", "mm", "chm", "gm", "lm", "mb", "mbe", "me", "mh", "mme", "mn", "tm"],
    "N": ["n", "nn", "cn", "dn", "gn", "gne", "kn", "ln", "mn", "mp", "nd", "ne", "ng", "nh", "nne", "nt", "pn", "sne"],
    "NG": ["ng", "n", "nc", "nd", "ngh", "ngue"],
    "P": ["p", "pp", "gh", "pe", "ph", "ppe"],
    "B": ["b", "bb", "be", "bh", "pb"],
    "T": ["t", "tt", "bt", "cht", "ct", "d", "ed", "ght", "pt", "te", "th", "tte", "tw"],
    "D": ["d", "dd", "de", "dh", "ed", "ld", "t"],
    "K": ["c", "k", "cc", "cch", "ch", "ck", "cq", "cqu", "cque", "cu", "ke", "kh", "kk", "lk", "q", "qu", "que", "x"],
    "G": ["g", "gg", "ckg", "gge", "gh", "gu", "gue"],
    "S": ["s", "ss", "c", "cc", "ce", "ps", "sc", "sce", "se", "sse", "st", "sth", "sw", "ts", "tsw", "tz", "z"],
    "Z": ["z", "zz", "cz", "s", "sc", "se", "sp", "ss", "sth", "ts", "tz", "x", "ze"],
    "SH": ["sh", "c", "ce", "ch", "che", "chi", "chsi", "ci", "s", "sc", "sch", "sci", "she", "shi", "si", "ss", "ssi", "ti"],
    "ZH": ["g", "ge", "j", "s", "si", "ti", "z", "zh", "zi"],
    "F": ["f", "ff", "fe", "ffe", "gh", "lf", "ph", "phe", "pph", "v", "ve"],
    "V": ["v", "vv", "f", "lve", "ph", "ve", "w"],
    "TH": ["th", "the", "chth", "phth", "tth"],
    "DH": ["th", "the"],
    "Y": ["y", "i", "j", "ll", "r"],
    "HH": ["h", "wh", "j", "ch", "x"],
    "R": ["r", "rr", "l", "re", "rh", "rre", "rrh", "rt", "wr"],
    "L": ["l", "ll", "le", "lh", "lle"],
    "W": ["w", "ww", "u", "o", "ou", "we", "wh"],
    "CH": ["ch", "tch", "c", "cc", "che", "chi", "cz", "t", "tche", "te", "th", "ti", "ts", "tsch", "tsh", "tz", "tzs", "tzsch"],
    "JH": ["g", "j", "ch", "d", "dg", "dge", "di", "dj", "ge", "gg", "gi", "jj", "t"],
    "KS": ["x", "xx", "cast", "cc", "chs", "cks", "cques", "cs", "cz", "kes", "ks", "lks", "ques", "xc", "xe", "xs", "xsc", "xsw"]
}


def phonemes(word):
    return arpabet[word][0]


def find_grapheme(word, phoneme):
    possible_graphemes = consonants[phoneme]

    for i in range(1, len(word) + 1):
        sub = word[:i]

        for grapheme in possible_graphemes:
            if grapheme in sub:
                return sub[:len(sub) - len(grapheme)], grapheme


def vowels(grapheme):
    regex = re.compile(r".*([aeiou]+)$")
    v = regex.match(grapheme)

    if v is None:
        return ""
    else:
        return v.group(1)


def graphemes(word):
    word_phonemes = phonemes(word)
    split_word = []

    for phoneme in word_phonemes:
        if phoneme in consonants.keys():
            extra, grapheme = find_grapheme(word, phoneme)
            vowel = vowels(extra)

            if vowel != "":
                split_word.append(vowel)

            split_word.append(phoneme)
            word = word[len(extra) + len(grapheme):]
        else:
            continue

    vowel = vowels(word)

    if vowel != "":
        split_word.append(vowel)

    return split_word


def misspell(word):
    word_graphemes = graphemes(word)

    for g in range(len(word_graphemes)):
        grapheme = word_graphemes[g]

        if grapheme in consonants.keys():
            word_graphemes[g] = random.choice(consonants[grapheme])

    return "".join(word_graphemes)

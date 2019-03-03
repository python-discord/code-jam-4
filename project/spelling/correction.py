import project.spelling.data as data


words = data.frequency_list()


def distance1(word):
    """All edits that are one edit away from `word`."""
    letters = "abcdefghijklmnopqrstuvwxyz"
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [L + R[1:] for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
    replaces = [L + c + R[1:] for L, R in splits if R for c in letters]
    inserts = [L + c + R for L, R in splits for c in letters]

    return set(deletes + transposes + replaces + inserts)


def is_correct(word):
    return word in words.keys()


def correction(word):
    """Given a word, offers a correction to that word"""
    short_coeff = 50
    long_coeff = 10

    if is_correct(word):
        dist0_freq = words[word]
    else:
        dist0_freq = 0

    dist1 = distance1(word)
    dist1_word = sorted(dist1, key=lambda w: words[w] if w in words.keys() else 0)[-1]

    if dist1_word in words.keys():
        dist1_freq = words[dist1_word]
    else:
        dist1_freq = 0

    dist2_word = ""
    dist2_freq = 0

    for w in dist1:
        dist2 = [x for x in distance1(w) if x in words.keys() and x not in dist1]

        if not dist2:
            continue

        current_word = sorted(dist2, key=lambda x: words[x])[-1]
        current_freq = words[current_word]

        if current_freq > dist2_freq:
            dist2_word = current_word
            dist2_freq = current_freq

    if dist0_freq == dist1_freq == dist2_freq == 0:
        raise NameError(f"Word {word} cannot be corrected")

    if len(word) < 6:
        if dist2_freq >= dist1_freq * short_coeff:
            return dist2_word
        elif dist1_freq >= dist0_freq * short_coeff:
            return dist1_word
        else:
            return word
    else:
        if dist2_freq >= dist1_freq * long_coeff:
            return dist2_word
        elif dist1_freq >= dist0_freq * long_coeff:
            return dist1_word
        else:
            return word

import base64
import string
import zlib


with open("./data/frequency_list.txt", "rb") as file:
    contents = zlib.decompress(base64.b64decode(file.read())).decode("utf-8")
    words = {}

    for tup in contents.split(";"):
        tup = tup.split(":")
        key, value = tup[0], int(tup[1])

        words[key] = value


def distance1(word: str) -> [str]:
    letters = string.ascii_lowercase
    dist1_words = []

    # Deletion
    for i in range(len(word)):
        dist1_words.append(word[:i] + word[i + 1:])

    for letter in letters:
        for j in range(len(word)):
            char = word[j]

            # Insertion
            dist1_words.append(word[:j] + letter + word[j:])

            # Substitution
            if letter != char:
                dist1_words.append(word[:j] + letter + word[j + 1:])

        dist1_words.append(word + letter)

    return dist1_words


def correction(word: str):
    coefficient = 20

    if word in words.keys():
        return word

    dist1_words = distance1(word)

    top_dist1_word = sorted(
        dist1_words,
        key=lambda w: words[w] if w in words.keys() else 0
    )[-1]
    
    top_dist1_freq = words[top_dist1_word]

    top_dist2_word = ""
    top_dist2_freq = 0

    for w in dist1_words:
        dist2_words = [x for x in distance1(w) if x in words.keys() and x not in dist1_words]

        if not dist2_words:
            continue

        current_word = sorted(dist2_words, key=lambda x: words[x])[-1]
        current_freq = words[current_word]

        if current_freq > top_dist2_freq:
            top_dist2_word = current_word
            top_dist2_freq = current_freq

    if top_dist1_freq >= top_dist2_freq * coefficient:
        return top_dist1_word
    else:
        return top_dist2_word


print(correction("therfe"))

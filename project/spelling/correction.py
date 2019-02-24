import base64
import string
import zlib


with open("./data/frequency_list.txt", "rb") as file:
    contents = zlib.decompress(base64.b64decode(file.read())).decode("utf-8")
    words = {}

    for word in contents.split(";"):
        word = word.split(":")
        print(word)
        key = word[0]
        value = int(word[1])

        words[key] = value


def distance_one(word: str) -> [str]:
    letters = string.ascii_lowercase
    words = []

    # Deletion
    for i in range(len(word)):
        words.append(word[:i] + word[i + 1:])

    for letter in letters:
        for j in range(len(word)):
            char = word[j]

            # Insertion
            words.append(word[:j] + letter + word[j:])

            # Substitution
            if letter != char:
                words.append(word[:j] + letter + word[j + 1:])

        words.append(word + letter)

    return words


def distance_two(word: str) -> [str]:
    pass


def correction(word: str):
    if word in words:
        return word


print(distance_one("abcd"))

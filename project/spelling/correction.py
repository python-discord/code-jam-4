import base64, zlib


def to_tup(string) -> (str, int):
    split = string.split(":")
    return split[0], int(split[1])


with open("./data/frequency_list.txt", "rb") as file:
    contents = zlib.decompress(base64.b64decode(file.read()))
    words = [to_tup(i) for i in contents.split(",")]


def correction(word: str):
    if word in words:
        return word

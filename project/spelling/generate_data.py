import base64, nltk, re, zlib


def corpus_downloaded(name: str) -> bool:
    """
    Checks if NLTK contains a certain corpus.
    :param name: the name of the corpus
    :return: whether that corpus is downloaded or not
    """
    try:
        nltk.data.find(f"corpora/{name}")
        return True
    except LookupError:
        return False


def frequency_list():
    """
    Creates `frequency_list.txt in `spelling/data`, which is a list of
    words sorted from most common to least common.
    """
    # Check if the `brown` corpus is downloaded
    if not corpus_downloaded("brown"):
        nltk.download("brown")

    # List of words from `brown`
    words = nltk.corpus.brown.words()
    # Sort those words by how common they are
    unfiltered = nltk.FreqDist(i.lower() for i in words).most_common()
    # Remove punctuation
    freq_list = [i for i in unfiltered if re.match(r"[A-Za-z]", i[0])]

    # Write the contents in
    with open("./data/frequency_list.txt", "wb") as file:
        freq_list = map(lambda tup: f"{tup[0]}:{tup[1]}", freq_list)
        contents = ",".join(freq_list)
        compressed = base64.b64encode(zlib.compress(contents.encode("utf-8"), 9))

        file.write(compressed)
        file.close()


frequency_list()

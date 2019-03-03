import nltk
import re


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


def arpabet():
    if not corpus_downloaded("cmudict"):
        nltk.download("cmudict")

    return nltk.corpus.cmudict.dict()


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
    freq_list = {i[0]: i[1] for i in unfiltered if re.match(r"[A-Za-z]", i[0])}

    return freq_list

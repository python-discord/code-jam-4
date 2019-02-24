"""The backend of the traslation."""
from googletrans import Translator

translator = Translator()


def translate(inp, lang: str):
    """
    Translates text from english to another language.

    Parameters:
        - list/string - a text you want to translate
        - string - the language you want to translate into
    Returns:
        - string - the translated text.
    """
    return translator.translate(inp, dest=lang).text

#not done yet, feel free to change it :p

class PredictiveText():

    def _update_text(text):
        text = text.lower()
        text = text.split()
        new_text = ''
        if 'hello' in text:
            text[text.index('hello')] = 'help me'

        new_text.join(text)
        return new_text
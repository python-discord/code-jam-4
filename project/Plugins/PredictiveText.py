#not done yet, feel free to change it :p

class PredictiveText():

    def _update_text(text):
        text = text.split()
        if 'hello' in text:
            text[text.index('hello')] = 'help me' #chage this to what ever you want
        return text
    
print(PredictiveText._update_text(text = 'hello'))
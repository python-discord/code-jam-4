from tkinter import INSERT


class WordReverser:

    def __init__(self):
        self.last_idx = '0'

    def reverse_word_only(self, event):
        widget = event.widget
        current_insert_index = widget.index('insert')
        current_line = current_insert_index.split('.')[0]

        # remove the char entered
        widget.delete("%s-1c" % INSERT, INSERT)

        # handle the enter key
        if event.char == '\r':
            widget.insert('end', '\n')
            self.last_idx = '0'
        elif event.char == ' ':
            # we got the word, set the new char index for next word
            self.last_idx = current_insert_index.split('.')[1]
        # finally put the char in reverse
        widget.insert(f"{current_line}.{self.last_idx}", event.char)

    def reverse_words_with_line(self, event):
        ta = event.widget
        event.widget.delete("%s-1c" % INSERT, INSERT)
        if event.char == '\r':
            ta.insert('end', '\n')
        else:
            line = ta.index('insert').split('.')[0]
            ta.insert(f"{line}.0", event.char)

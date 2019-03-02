import tkinter as tk
from tkinter import *
from random import randint
from project.AlphabetGuesser.letter_guesser import LetterGuesser


class AlphabetGuesserInter(tk.Frame):

    def __init__(self, master, current_entry, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.letter_guesser = LetterGuesser()

        self.current_entry = current_entry
        self.current_entry_label = None
        self.letters_input = None
        self.header = None
        self.description = None
        self.title_label = None
        self.current_letter_id = 1
        self.question_label = None
        self.current_word = None
        self.button_1 = None
        self.button_2 = None
        self.submit_button = None

        self.__letter_found = False

        self.create()

    def create(self):
        self.header = tk.Label(self, text="EntryBot 3000", font="Calibri 20")
        self.description = tk.Label(self, text="The latest in typing technology since 700 B.C\n\n",
                                    font="Calibri 10")

        self.title_label = tk.Label(self,
                                    text="You are entering {} {}:\nAnswer the questions below to fill out the entry\n"
                                         "".format(self.get_prefix(self.current_entry), self.current_entry),
                                    font="Calibri 11")
        self.question_label = tk.Label(self,
                                       text="Is your {} character contained in the phrase :"
                                            "".format(self.complete_number(self.current_letter_id)),
                                       font="Calibri 11")

        self.current_word = tk.Label(self, font="Calibri 18", relief="sunken")
        self.update_current_asked_word()

        self.button_1 = tk.Button(self, command=lambda: self.send_answer(self.button_1['text']))
        self.button_2 = tk.Button(self, command=lambda: self.send_answer(self.button_2['text']))
        self.button_1.config(font="Calibri 15")
        self.button_2.config(font="Calibri 15")
        self.randomize_buttons()

        self.current_entry_label = tk.Label(self, text=self.current_entry + " :", font="Calibri 12")
        self.letters_input = tk.Label(self, relief="sunken", font="Calibri 15")

        self.submit_button = tk.Button(self, text="Submit", font="Calibri 15", command=lambda: self.submit())

        self.header.grid(row=0, column=0, columnspan=2, sticky=N + S + E + W)
        self.description.grid(row=1, column=0, columnspan=2, sticky=N + S + E + W)

        self.title_label.grid(column=0, row=2, columnspan=2, sticky=N + S + E + W)
        self.question_label.grid(column=0, row=3, columnspan=2, sticky=N + S + E + W)
        self.current_word.grid(column=0, row=4, columnspan=2, padx=10, pady=10, sticky=N + S + E + W)

        self.button_1.grid(column=0, row=5, sticky=N + S + E + W)
        self.button_2.grid(column=1, row=5, sticky=N + S + E + W)

        self.current_entry_label.grid(column=0, row=6, columnspan=2, sticky=N + S + E + W)
        self.letters_input.grid(column=0, row=7, columnspan=2, padx=10, sticky=N + S + E + W)
        self.submit_button.grid(column=0, row=8, columnspan=2, padx=10, pady=10, sticky=N + S + E + W)

    def update_current_asked_word(self):
        self.current_word['text'] = '"' + self.letter_guesser.request_word() + '"'

    def send_answer(self, answer):
        if self.__letter_found and answer == "Yes":
            self.current_letter_id += 1
            if self.question_label['text'] == "I found your character! Continue?":
                self.question_label['text'] = "Is your {} character contained in the phrase :"\
                    "".format(self.complete_number(self.current_letter_id))
            self.restart_letter_guesser()
            return
        elif self.__letter_found and answer == "No":
            # Return the current output and go back to the main window
            self.submit()
            return
        self.letter_guesser.answer(self.current_word['text'], answer)
        self.randomize_buttons()

        print(self.letter_guesser.possible_characters)
        if len(self.letter_guesser.possible_characters) == 1:
            self.letter_found()
        else:
            self.update_current_asked_word()

    def letter_found(self):
        self.question_label['text'] = "I found your character! Continue?"
        self.current_word['text'] = self.letter_guesser.possible_characters[0].upper()
        if len(self.letters_input['text']) == 0 or self.letters_input['text'][-1] == " ":
            self.letters_input['text'] = self.letters_input['text'] + self.letter_guesser.possible_characters[0].upper()
        else:
            self.letters_input['text'] = self.letters_input['text'] + self.letter_guesser.possible_characters[0]
        self.__letter_found = True

    def randomize_buttons(self):
        if randint(0, 1) == 1:
            self.button_1['text'] = 'Yes'
            self.button_2['text'] = 'No'
        else:
            self.button_1['text'] = 'No'
            self.button_2['text'] = 'Yes'

    def submit(self):
        print("Submitted")

    @staticmethod
    def get_prefix(word):
        if word[0] in ['A', 'E', 'I', 'O', 'U']:
            return 'an'
        return 'a'

    @staticmethod
    def complete_number(number):
        if number == 1:
            return '1st'
        elif number == 2:
            return '2nd'
        elif number == 3:
            return '3rd'
        else:
            return str(number) + 'th'

    def restart_letter_guesser(self):
        self.letter_guesser.__init__()
        self.update_current_asked_word()
        self.__letter_found = False


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry("300x400")
    root.resizable(False, False)
    a = AlphabetGuesserInter(root, "Name", width=300, height=500)

    a.grid(row=0, column=0)
    root.mainloop()

import tkinter as tk
from random import randint
from project.AlphabetGuesser.letter_guesser import LetterGuesser

class AlphabetGuesserInter(tk.Frame):

    def __init__(self, master, current_entry, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.frame = tk.Frame()
        self.letter_guesser = LetterGuesser()

        self.current_entry = current_entry
        self.letters_input = None
        self.title_label = None
        self.current_letter_id = 1
        self.question_label = None
        self.current_word = None
        self.button_1 = None
        self.button_2 = None

        self.__letter_found = False

        self.create()

    def create(self):

        self.current_entry = tk.Label(self, text=self.current_entry+" :")
        self.letters_input = tk.Label(self, text="")

        self.title_label = tk.Label(self.frame, text="Please answer these few questions\n and we will automatically \ncomplete your " +
                                    "contact information!", font=("Calibri 14"))
        self.question_label = tk.Label(self.frame, text="Is your " + self.complete_number(self.current_letter_id) +
                                 ' character in the word :')
        self.current_word = tk.Label(self.frame, font=("Calibri 20"))
        self.update_current_asked_word()

        self.button_1 = tk.Button(self.frame, command= lambda: self.send_answer(self.button_1['text']))
        self.button_2 = tk.Button(self.frame, command=lambda: self.send_answer(self.button_2['text']))
        self.randomize_buttons()

        self.current_entry.grid(column=0, row=0)
        self.letters_input.grid(column=1, row=0, sticky='W')

        self.button_1.grid(column=0, row=4)
        self.button_2.grid(column=1, row=4)

        self.title_label.grid(column=0, row=1, columnspan=2)
        self.question_label.grid(column=0, row=2, columnspan=2)
        self.current_word.grid(column=0, row=3, columnspan=2)
        self.frame.grid(row=1, column=0, sticky='S')

    def update_current_asked_word(self):
        self.current_word['text'] = '"' + self.letter_guesser.request_word() + '"'

    def send_answer(self, answer):
        if self.__letter_found and answer == "Yes":
            self.restart_letter_guesser()
            return
        self.letter_guesser.answer(self.current_word['text'], answer)
        self.randomize_buttons()

        print(self.letter_guesser.possible_characters)
        if len(self.letter_guesser.possible_characters) == 1:
            self.letter_found()
        else:
            self.update_current_asked_word()

    def letter_found(self):
        self.question_label['text'] = "I found your character! \nDo you want to add some more?"
        self.current_word['text'] = self.letter_guesser.possible_characters[0].upper()
        if len(self.letters_input['text']) == 0 or self.letters_input['text'][-1]==" ":
            self.letters_input['text'] = self.letters_input['text'] + self.letter_guesser.possible_characters[0].upper()
        else:
            self.letters_input['text'] = self.letters_input['text'] + self.letter_guesser.possible_characters[0]
        self.__letter_found = True

    def randomize_buttons(self):
        if randint(0,1) == 1:
            self.button_1['text'] = 'Yes'
            self.button_2['text'] = 'No'
        else:
            self.button_1['text'] = 'No'
            self.button_2['text'] = 'Yes'

    def complete_number(self, number):
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

    a.grid(row=0,column=0)
    root.mainloop()
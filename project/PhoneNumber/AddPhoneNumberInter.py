import tkinter as tk
from project.PhoneNumber.PhoneCanvas import PhoneCanvas, PhoneButton


class AddPhoneNumberInter(tk.Frame):

    def __init__(self, master):
        # TODO -> Create the whole interface for when the user wishes to add a phone number to a contact.
        super().__init__(master)
        self.master = master
        self.entry = PhoneNumberEntry(self)
        self.phone_canvas = PhoneCanvas(self.master, self.entry)
        self.master.bind("<<Send_Phone_Number>>", self.__get_phone_number)

        self.entry.pack()
        self.pack()

    def __get_phone_number(self, event):
        number = self.phone_canvas.send_output_number()
        if number is not None:
            self.add_phone_number_to_entry(number)

    def add_phone_number_to_entry(self, num: int):
        self.entry.add_phone_number(num)



class PhoneNumberEntry(tk.Entry):

    def __init__(self, master):
        super().__init__(master)

    def add_phone_number(self, num: int):
        current_text = self.get()
        current_length = len(current_text)
        if current_length == 12:
            return
        if current_length == 3 or current_length == 7:
            self.insert('end', '-')
        self.insert('end', num)

    def clear_phone_number(self):
        self.delete(0, 'end')

if __name__ == '__main__':
    root = tk.Tk()
    root.geometry("800x800")
    AddPhoneNumberInter(root)
    root.mainloop()
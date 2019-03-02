import tkinter as tk
from project.PhoneNumber.PhoneCanvas import PhoneCanvas


class AddPhoneNumberInter(tk.Frame):
    """
    This class is the frame that contains PhoneCanvas with the label that shows the phone number as the user
    dials them. It gives the option of erasing the whole phone number.

    === Public Attributes ===
        master: root of the frame
        text_label: Label with the text saying what the user should do
        label_frame: Frame containing the phone number label and button
        phone_number_label: Label in which the dialed number will be written
        button: Button to clear the phone_number label.

        === Methods ===
        add_phone_number_to_entry: This method adds one number to the self.phone_number_label text
    """

    def __init__(self, master, *args, **kwargs, ):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.page_name = 'Add Phone Number'
        self.text_label = tk.Label(self, font=('Calibri', 10), fg='#63FF20', bg='#00536a', borderwidth=2,
                                   text="Please enter the phone number you wish\n to add with the rotary phone below.")

        self.label_frame = tk.Frame(self, bg='#00536a')
        self.phone_number_label = PhoneNumberLabel(self.label_frame, font=('Calibri', 20), fg='#63FF20', bg='#00536a',
                                                   width=12, borderwidth=2, relief='sunken')

        self.button = tk.Button(self.label_frame, text='Clear', bg='#00536a', font=('Calibri', 14), height=1,
                                command=self.phone_number_label.clear_phone_number)

        self.text_label.grid(row=0, column=0)
        self.phone_number_label.grid(row=0, column=0)
        self.button.grid(row=0, column=1)
        self.label_frame.grid(row=1, column=0)

        self.phone_canvas = PhoneCanvas(self)
        self.phone_canvas.grid(row=2, column=0)
        self.grid(row=0, column=0)

        self.master.bind("<<Send_Phone_Number>>", self.__get_dialed_number)

    def add_phone_number_to_entry(self, num: str) -> None:
        """
        This method adds one number to the phone number label.
        :param num: Number we which to add to the phone number label.
        :return: None
        """
        self.phone_number_label.add_phone_number(num)

    def get_complete_phone_number(self):
        if len(self.phone_number_label['text']) == 12:
            return self.phone_number_label['text']
        else:
            return ""

    def __get_dialed_number(self, event) -> None:
        """
        This method gets the phone number from the PhoneCanvas, it is called by the <<Send_Phone_Number>> event.
        :param event:
        :return: None
        """
        number = self.phone_canvas.send_output_number()
        if number is not None:
            self.add_phone_number_to_entry(number)
            if len(self.phone_number_label['text']) == 12:
                self.master.event_generate("<<Phone Number Complete>>")


class PhoneNumberLabel(tk.Label):
    """
    PhoneNumberLabel is a simple class inherited from tk.Label. It allows the user to add one number at the time and
    will keep the ###-###-#### formatting.
    === Public Attributes ===

    === Methods ===
    add_phone_number: This method adds one number to the displayed text. It automatically adds '-' to keep the
    ###-###-#### formatting.
    clear_phone_number: This method erases all the number that were displayed on the label.
    """

    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

    def add_phone_number(self, num: int) -> None:
        """
        This method adds a number to the label, it automatically adds '-' at the right location in order to keep the
        ###-###-#### formatting.
        :param num: Number we wish to add to the label.
        :return: None
        """
        current_text = self['text']
        current_length = len(current_text)
        if current_length == 3 or current_length == 7:
            self['text'] = self['text'] + '-'
        self['text'] = self['text'] + num

    def clear_phone_number(self) -> None:
        """
        This method clears the phone number displayed in the label.
        :return: None
        """
        self['text'] = ''


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry("300x400")
    root.configure(background='#00536a')
    root.resizable(False, False)
    AddPhoneNumberInter(root, bg='#00536a')
    root.mainloop()

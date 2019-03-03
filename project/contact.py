from typing import List, Dict


class Contact:
    """
    Class for Contacts

    === Public Attributes ===
    name: Name of the contact
    phone_numbers: All phone numbers of the contact
    email_addresses: All email addresses of the contact
    addresses: All physical addresses of the contact
    notes: Any notes the user wishes to leave for the contact

    === Methods ===
    change_name: Allows the user to change the name of the contact
    add_phone_number: Allows the user to add a phone number to any of the
                      categories Home, Work or Personal
    change_phone_number: Allows the user to change a number already entered, if
                         the number does not exist then nothing is done.
                         If the new_num param is '', then the number is removed
    add_address: Allows the user to add either an email address or a physical
                 address to the contact
    change_email_address: Allows the user to change an email address already
                          entered if the address does not exist then nothing is
                          done. If the new_add param is '', then the address is
                          removed
    change_address: Allows the user to change an email address already entered
                    if the address does not exist then nothing is done.
                    If the new_add param is '', then the address is removed

    new_note: Allows the user to leave a note for the contact
    change_note: Allows the user to change a note already entered, if the note
                 doesn't exist then nothing is done. If the new_note param is ''
                 then the notes is deleted

    """
    name: str
    phone_numbers: Dict[str, List[str]]
    email_addresses: List[str]
    addresses: List[str]
    notes: [str]

    def __init__(self, name: str) -> None:
        self.name = name
        self.phone_numbers = {'Home': [], 'Work': [], 'Personal': []}
        self.email_addresses = []
        self.addresses = []
        self.notes = []

    def change_name(self, new_name: str) -> None:
        """
        Method allows the user to change the name of the contact
        :param new_name: Name to be changed to
        :return: None
        """
        print("DEBUG: Set Name To:", new_name)
        self.name = new_name

    def add_phone_number(self, num_type: str, number: str) -> None:
        """
        Method allows the user to add a new phone number for the contact
        :param num_type: Home or Work or Personal. The type of phone number that
        is being assigned
        :param number: The phone number that is being assigned
        :return: None
        """
        if num_type in ['Home', 'Work', 'Personal']:
            print("DEBUG: Phone Number:", number)
            print("DEBUG: Num_type:", num_type)
            self.phone_numbers[num_type].append(number)

    def change_phone_number(self, orig_num: str, new_num: str) -> None:
        """
        Method allows the user to change a phone number
        :param orig_num: The original number to be changed
        :param new_num: The number to be changed to
        :return: None
        """
        if orig_num in self.phone_numbers['Home']:
            self.phone_numbers['Home'].remove(orig_num)
            if new_num != '':
                self.phone_numbers['Home'].append(new_num)

        elif orig_num in self.phone_numbers['Work']:
            self.phone_numbers['Work'].remove(orig_num)
            if new_num != '':
                self.phone_numbers['Work'].append(new_num)

        elif orig_num in self.phone_numbers['Personal']:
            self.phone_numbers['Personal'].remove(orig_num)
            if new_num != '':
                self.phone_numbers['Personal'].append(new_num)

    def add_address(self, address_type: str, address: str) -> None:
        """
        Method allows the user to add a new address for the contact
        :param address_type: Physical or Email. The type of phone number that
        is being assigned
        :param address: The phone number that is being assigned
        :return: None
        """
        if address_type == 'Physical':
            self.addresses.append(address)

        elif address_type == 'Email':
            self.email_addresses.append(address)

    def change_email_address(self, orig_add: str, new_add: str) -> None:
        """
        Method allows the user to change a phone number
        :param orig_add: The original email address to be changed
        :param new_add: The email address to be changed to
        :return: None
        """
        if orig_add in self.email_addresses:
            self.email_addresses.remove(orig_add)
            if new_add != '':
                self.email_addresses.append(new_add)

    def change_address(self, orig_add: str, new_add: str) -> None:
        """
        Method allows the user to change a phone number
        :param orig_add: The original address to be changed
        :param new_add: The address to be changed to
        :return: None
        """
        if orig_add in self.addresses:
            self.addresses.remove(orig_add)
            if new_add != '':
                self.addresses.append(new_add)

    def add_note(self, note: str) -> None:
        """
        Method allows the user to add a note
        :param note: The note to be added
        :return: None
        """
        self.notes.append(note)

    def change_note(self, orig_note: str, new_note: str) -> None:
        """
        Method allows the user to change a note
        :param orig_note: The original note to be changed
        :param new_note: The note to be changed to
        :return: None
        """
        if orig_note in self.notes:
            self.notes.remove(orig_note)
            if new_note != '':
                self.notes.append(new_note)

    def __str__(self):
        text_to_print = "Contact: \nName: " + str(self.name) + "\n"
        text_to_print += "Work phone number: " + str(self.phone_numbers["Work"]) + "\n"
        text_to_print += "Home phone number: " + str(self.phone_numbers["Home"]) + "\n"
        text_to_print += "Personal phone number: " + str(self.phone_numbers["Personal"]) + "\n"
        text_to_print += "Email address: " + str(self.email_addresses) + "\n"
        text_to_print += "Home address: " + str(self.addresses) + "\n"
        text_to_print += "Notes: " + str(self.notes) + "\n"

        return text_to_print

from tkinter import *
from tkinter.ttk import *
from project.contact import Contact
import pickle
import sys

"""
TODO:
Fix scrolling with mousewheel in ContactsPage
Make preview_field in AddContactsPage update when an contact attribute is added
Settings Page:
- Change color schemes; all options are terrible color palettes
- Change fonts; all options are terrible fonts
"""


class Controller(Tk):
    """
    Controller Class:
    - Serves as a hub for every page contained in the UI, allows for the flow of information between pages
    - Acts as the container for ContactsPage, AddContactsPage, and SettingsPage by making use of ttk.Notebook

    === Public Attributes ===
    notebook: Widget containing tabs; each page is assigned a tab, and can be navigated to easily
    frames: Dictionary of all pages; allows for access of information across pages
            e.g. If I wanted to call a method from a separate class:
                self.controller.frames[<name of page>].<method I want to call>()

    === Methods ===
    None
    """
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.resizable(False, False)
        self.geometry("300x400")
        self.title("Contact Manager")
        self.iconbitmap("src/Phone.ico")
        for i in range(5):
            self.rowconfigure(i, weight=1)
            self.columnconfigure(i, weight=1)

        self.frames = {}

        self.notebook = Notebook(self)
        self.notebook.grid(row=0, column=0, columnspan=5, rowspan=5, sticky=N+S+E+W)

        for page in [ContactsPage, AddContactPage, SettingsPage]:
            frame = page(self.notebook, self)
            self.notebook.add(frame, text=frame.page_name)
            self.frames[frame.page_name] = frame


class ContactsPage(Frame):
    """
    Contacts Page:
        Contains the list of currently added contacts

    === Public Attributes ===
    master: The frame containing all information on this page
    controller: Reference to the Controller Class

    page_name: String containing a name for this page; used for setting the tabs
                in the containing notebook

    contacts_list: Dictionary of contacts, each contact is a Contact class instance,
                    each key is the name of the contact

    scroll_bar: Scroll bar that controls what is viewable in the contacts list;
                won't scroll if nothing is in the list, or everything is already
                shown.
    contacts_field: Area where contacts are shown; 10 at a time
    letters_field: Listbox that shows each letter of the alphabet to help the user find
                    contact they're looking for
    show_info: Button that updates the info_field with the information of the
                currently selected contact
    delete: Button that deletes the selected contact
    info_field: Listbox that contains the information of the currently selected contact
    info_scroll: Scrollbar that controls what is viewable in the info_field; won't
                    scroll if nothing is in the list, or everything is already shown

    self.load: Button to load contacts
    self.save: Button to save contacts

    === Methods ===
    create: Initializes objects & places them on the page
    insert_contact: Adds a contact's name to the end of the contacts field
    show_contact_info: Shows the information of the selected contact in the info listbox
    delete_contact: Deletes the selected contact & reloads the contacts Listbox
    clear_fields: Clears both fields on the contacts page
    load_contacts: Loads contacts in from a file
    save_contacts: Saves contacts as a file
    yview: Adjusts the view of contacts_field & letters_field at the same time
    """
    def __init__(self, master, controller, **kw):
        super().__init__(master, **kw)
        self.master = master
        self.controller = controller

        self.page_name = "View Contacts"

        # Initialize object names
        self.contacts_list = {}

        self.scroll_bar = None
        self.contacts_field = None
        self.letters_field = None
        self.show_info = None
        self.delete = None
        self.info_field = None
        self.info_scroll = None

        self.load = None
        self.save = None

        # Create objects
        self.create()

    def create(self) -> None:
        self.info_scroll = Scrollbar(self, orient=VERTICAL)
        self.info_field = Listbox(
            self,
            yscrollcommand=self.info_scroll.set
        )
        self.info_scroll.config(command=self.info_field.yview)
        self.info_field.grid(row=3, column=0, columnspan=5, sticky=N+S+E+W)
        self.info_scroll.grid(row=3, column=5, sticky=N+S+E+W)

        self.delete = Button(self, text="Delete", command=lambda: self.delete_contact())
        self.delete.grid(row=2, column=3, columnspan=3, sticky=N+S+E+W)

        self.show_info = Button(self, text="Show Info", command=lambda: self.show_contact_info())
        self.show_info.grid(row=2, column=0, columnspan=3, sticky=N+S+E+W)

        self.scroll_bar = Scrollbar(self)
        self.contacts_field = Listbox(
            self,
            yscrollcommand=self.scroll_bar.set,
            selectmode=SINGLE
        )
        self.letters_field = Listbox(
            self,
            width=2,
            yscrollcommand=self.scroll_bar.set,
            selectmode=SINGLE
        )
        self.contacts_field.grid(row=1, column=0, columnspan=5, sticky=N+S+E+W)
        self.letters_field.grid(row=1, column=4, sticky=N+S+E+W)
        self.scroll_bar.grid(row=1, column=5, sticky=N+S+E+W)
        self.scroll_bar.config(command=self.yview)

        self.save = Button(
            self,
            text="Save Contacts",
            command=lambda: self.save_contacts()
        )
        self.save.grid(row=0, column=3, columnspan=4, sticky=N+S+E+W)

        self.load = Button(
            self,
            text="Load Contacts",
            command=lambda: self.load_contacts()
        )
        self.load.grid(row=0, column=0, columnspan=3, sticky=N+S+E+W)

        for i in range(3):
            self.grid_rowconfigure(i, weight=1)

        for i in range(4):
            self.grid_columnconfigure(i, weight=1)

    def yview(self, *args) -> None:
        self.contacts_field.yview(*args)
        self.letters_field.yview(*args)

    def delete_contact(self) -> None:
        name = self.contacts_field.get(self.contacts_field.curselection()[0])
        del self.contacts_list[name]
        self.clear_fields()
        for contact in sorted(self.contacts_list):
            self.insert_contact(contact)

    def clear_fields(self) -> None:
        for field in [self.contacts_field, self.info_field, self.letters_field]:
            field.delete(0, END)

    def refresh_fields(self) -> None:
        self.clear_fields()
        letter = ''
        for contact in sorted(self.contacts_list):
            if contact[0] != letter:
                letter = contact[0]
                self.letters_field.insert(END, letter)
            else:
                self.letters_field.insert(END, '')
            self.contacts_field.insert(END, contact)

    def load_contacts(self) -> None:
        with open("contacts_pickle", 'rb') as infile:
            self.contacts_list = pickle.load(infile)
            self.refresh_fields()

    def save_contacts(self) -> None:
        with open("contacts_pickle", 'wb') as outfile:
            pickle.dump(self.contacts_list, outfile)

    def insert_contact(self, contact) -> None:
        self.contacts_field.insert(END, contact)

    def show_contact_info(self) -> None:
        name = self.contacts_field.get(self.contacts_field.curselection()[0])
        contact = self.contacts_list[name]
        home_phone_nums = contact.phone_numbers["Home"]
        work_phone_nums = contact.phone_numbers["Work"]
        personal_phone_nums = contact.phone_numbers["Personal"]
        emails = contact.email_addresses
        addresses = contact.addresses
        notes = contact.notes
        self.info_field.delete(0, END)
        self.info_field.insert(END, name)
        self.info_field.insert(END, "")
        if len(home_phone_nums) or len(work_phone_nums) or len(personal_phone_nums) > 0:
            self.info_field.insert(END, "Phone:")
            for elem in home_phone_nums:
                self.info_field.insert(END, "   Home: " + elem)
            for elem in work_phone_nums:
                self.info_field.insert(END, "   Work: " + elem)
            for elem in personal_phone_nums:
                self.info_field.insert(END, "   Personal: " + elem)
        if len(emails) > 0:
            self.info_field.insert(END, "Emails:")
            for elem in emails:
                self.info_field.insert(END, "   " + elem)
        if len(addresses) > 0:
            self.info_field.insert(END, "Addresses:")
            for elem in addresses:
                self.info_field.insert(END, "   " + elem)
        if len(notes) > 0:
            self.info_field.insert(END, "Notes:")
            for elem in notes:
                self.info_field.insert(END, "   " + elem)


class AddContactPage(Frame):
    """
    Add New Contact Page:

    === Public Attributes ===
    master: The frame containing all information on this page
    controller: Reference to the Controller Class

    contact_new: Contact class instance that holds the data that the
                user inputs; when the user submits, the information is
                stored on the contacts_list in ContactsPage.

    Each contact has 5 attributes:
    - Name
    - Phone Number
    - Email
    - Address
    - Notes
    Each attribute has the corresponding objects on the page:
    - A Label
    - A Text Entry Box
    - A Button to add the information to the preview, & update the contact
    The only exception being the Phone Number, which requires the user to
        choose whether the phone number is for Home, Work, or Personal.
        This is done using a Radiobutton, which can only have one value
        chosen at a time. The value of the Radiobutton is tied to a
        StringVar called phone_type_var. When the user clicks 'Add' next
        to the phone number, the StringVar is passed into the
        add_phone_number method.

    clear: Button that clears all text entries
    add_to_contacts: Button that adds the current contact to the contact_list
                    on ContactsPage
    text_entries: List of all text entries; can be looped over to perform a
                    repetitive task on each entry. e.g Clearing all entries

    preview_scroll: Scrollbar that control what is viewable in the preview
                    Listbox
    preview: Listbox that shows the info of the contact being created currently

    === Methods ===
    create: Initializes objects & places them on the page
    add_contact: Adds contact to the contact_list in ContactsPage;
                If the contact is new, the name of the contact is added to
                the contacts Listbox on ContactsPage
    clear_all: Loops over all text entries and clears them
    add_phone_num: TEMPORARY METHOD; Used for debugging
    """
    def __init__(self, master, controller, **kw):
        super().__init__(master, **kw)
        self.master = master
        self.controller = controller

        self.page_name = "New Contact"

        # Initialize object names
        self.contact_new = Contact('')

        self.enter_name = None
        self.enter_name_label = None
        self.enter_name_button = None

        # PLACEHOLDER FOR ACTUAL PHONE NUMBER ENTRY
        self.enter_phone_num = None
        self.phone_type_home = None
        self.phone_type_work = None
        self.phone_type_personal = None
        self.enter_phone_num_label = None
        self.enter_phone_num_button = None
        self.phone_type_var = None

        self.enter_email = None
        self.enter_email_label = None
        self.enter_email_button = None

        self.enter_address = None
        self.enter_address_label = None
        self.enter_address_button = None

        self.enter_notes = None
        self.enter_notes_label = None
        self.enter_notes_button = None

        self.clear = None
        self.add_to_contacts = None

        self.preview_scroll = None
        self.preview = None

        self.text_entries = None

        # Create objects
        self.create()

    def create(self) -> None:
        self.preview_scroll = Scrollbar(self, orient=VERTICAL)
        self.preview = Listbox(
            self,
            yscrollcommand=self.preview_scroll.set
        )
        self.preview_scroll.config(command=self.preview.yview)
        self.preview.grid(row=8, column=0, columnspan=5, sticky=N+S+E+W)
        self.preview_scroll.grid(row=8, column=5, sticky=N+S+E+W)

        self.add_to_contacts = Button(self, text="Submit to Contacts", command=lambda: self.add_contact())
        self.add_to_contacts.grid(row=7, column=0, columnspan=2, sticky=N+S+E+W)

        self.clear = Button(self, text="Clear All", command=lambda: self.clear_all())
        self.clear.grid(row=7, column=2, sticky=N+S+E+W)

        self.enter_notes = Entry(self)
        self.enter_notes_label = Label(self, text="Notes:")
        self.enter_notes_button = Button(
            self,
            text="Add",
            command=lambda: self.contact_new.add_note(self.enter_notes.get()),
            width=5
        )
        self.enter_notes_button.grid(row=6, column=4, columnspan=2, sticky=N+S+E+W)
        self.enter_notes_label.grid(row=6, column=0, sticky=N+S+E+W)
        self.enter_notes.grid(row=6, column=1, columnspan=3, sticky=N+S+E+W)

        self.enter_address = Entry(self)
        self.enter_address_label = Label(self, text="Address")
        self.enter_address_button = Button(
            self,
            text="Add",
            command=lambda: self.contact_new.add_address("Physical", self.enter_address.get()),
            width=5
        )
        self.enter_address_label.grid(row=5, column=0, sticky=N+S+E+W)
        self.enter_address.grid(row=5, column=1, columnspan=3, sticky=N+S+E+W)
        self.enter_address_button.grid(row=5, column=4, columnspan=2, sticky=N+S+E+W)

        self.enter_email = Entry(self)
        self.enter_email_label = Label(self, text="Email:")
        self.enter_email_button = Button(
            self,
            text="Add",
            command=lambda: self.contact_new.add_address("Email", self.enter_email.get()),
            width=5
        )
        self.enter_email_label.grid(row=4, column=0, sticky=N+S+E+W)
        self.enter_email.grid(row=4, column=1, columnspan=3, sticky=N+S+E+W)
        self.enter_email_button.grid(row=4, column=4, columnspan=2, sticky=N+S+E+W)

        # PLACEHOLDER FOR ACTUAL PHONE NUMBER ENTRY
        self.enter_phone_num = Entry(self)
        self.enter_phone_num_label = Label(self, text="Phone:")
        phone_type_var = StringVar()
        self.phone_type_home = Radiobutton(self, text="Home", variable=phone_type_var, value="Home")
        self.phone_type_work = Radiobutton(self, text="Work", variable=phone_type_var, value="Work")
        self.phone_type_personal = Radiobutton(self, text="Personal", variable=phone_type_var, value="Personal")
        self.enter_phone_num_button = Button(
            self,
            text="Add",
            command=lambda: self.add_phone_num(phone_type_var.get(), self.enter_phone_num.get()),
            width=5
        )
        self.enter_phone_num_label.grid(row=2, column=0, sticky=N+S+E+W)
        self.enter_phone_num.grid(row=2, column=1, columnspan=3, sticky=N+S+E+W)
        self.phone_type_home.grid(row=3, column=0, sticky=N+S+E+W)
        self.phone_type_work.grid(row=3, column=1, sticky=N+S+E+W)
        self.phone_type_personal.grid(row=3, column=2, sticky=N+S+E+W)
        self.enter_phone_num_button.grid(row=2, column=4, columnspan=2, sticky=N+S+E+W)

        self.enter_name = Entry(self)
        self.enter_name_label = Label(self, text="Name:")
        self.enter_name_button = Button(
            self,
            text="Add",
            command=lambda: self.contact_new.change_name(self.enter_name.get()),
            width=5
        )
        self.enter_name_button.grid(row=1, column=4, columnspan=2, sticky=N+S+E+W)
        self.enter_name_label.grid(row=1, column=0, sticky=N+S+E+W)
        self.enter_name.grid(row=1, column=1, columnspan=3, sticky=N+S+E+W)

        self.text_entries = [self.enter_name, self.enter_phone_num, self.enter_email, self.enter_address,
                             self.enter_notes]

        for i in range(8):
            self.grid_rowconfigure(i, weight=1)

        for i in range(5):
            self.grid_columnconfigure(i, weight=1)

    def add_phone_num(self, num_type, num) -> None:
        if num_type != '':
            self.contact_new.add_phone_number(num_type, num)

    def add_contact(self) -> None:
        name = self.contact_new.name
        contacts_list = self.controller.frames["View Contacts"].contacts_list
        if name != '':
            if name not in contacts_list:
                print("DEBUG: Creating new contact")
                contacts_list[name] = self.contact_new
            elif name in contacts_list:
                print("DEBUG: Updating already existing contact")
                contacts_list[name] = self.contact_new
        else:
            print("DEBUG: Entered empty name")
        self.controller.frames["View Contacts"].contacts_list = contacts_list
        self.controller.frames["View Contacts"].clear_fields()
        for contact in sorted(contacts_list):
            self.controller.frames["View Contacts"].insert_contact(contact)
        self.contact_new = Contact('')

    def clear_all(self) -> None:
        for entry in self.text_entries:
            entry.delete(0, END)


class SettingsPage(Frame):
    """
        Settings Page:

        === Public Attributes ===
        master: The frame containing all information on this page
        controller: Reference to the Controller Class

        === Methods ===
        create: Initializes objects & places them on the page
        """
    def __init__(self, master, controller, **kw):
        super().__init__(master, **kw)
        self.master = master
        self.controller = controller

        self.page_name = "Settings"

        # Initialize object names

        # Create objects
        self.create()

    def create(self) -> None:
        pass


if __name__ == "__main__":
    app = Controller()
    app.mainloop()

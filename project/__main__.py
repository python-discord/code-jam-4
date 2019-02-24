from tkinter import *
from project.contact import Contact


class Controller(Tk):
    """
    Controller Class:

    === Public Attributes ===
    frames: Dictionary of all available pages

    === Methods ===
    show_frame: Allows the switching from one page to another.
                Each page is like a layer in a photo editor,
                calling 'frame.tkraise()' essentially brings
                the specified frame to the top layer, where
                it can be interacted with.
    """
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        container = Frame(self)
        container.pack(side=TOP, fill=BOTH, expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for page in [ContactsPage, AddContactPage, SettingsPage]:
            frame = page(container, self)
            self.frames[page] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(ContactsPage)

    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()


class ContactsPage(Frame):
    """
    Contacts Page:
        Contains the list of currently added contacts

    === Public Attributes ===
    master: The frame containing all information on this page
    controller: Reference to the Controller Class

    scroll_bar: Scroll bar that controls what is viewable in the contacts list;
                won't scroll if nothing is in the list, or everything is already
                shown.
    contacts_field: Area where contacts are shown; 10 at a time

    contacts: Button that takes the user to the 'Contacts' page
    new_contact: Button that takes the user to the 'Add New Contact' page
    settings: Button that takes the user to the 'Settings' page

    === Methods ===
    create: Initializes objects & places them on the page
    insert_contact: UNFINISHED; adds a contact to the end of the contacts field
    """
    def __init__(self, master, controller):
        Frame.__init__(self, master)
        self.master = master
        self.controller = controller

        # Initialize object names
        self.contacts_list = {}

        self.scroll_bar = None
        self.contacts_field = None
        self.show_info = None

        self.contacts = None
        self.new_contact = None
        self.settings = None

        # Create objects
        self.create()

    def create(self):
        self.show_info = Button(self, text="Show Info", command=lambda: self.show_contact_info())
        self.show_info.grid(row=2, column=0)

        self.contacts = Button(self, text="Contacts", command=lambda: self.controller.show_frame(ContactsPage))
        self.contacts.grid(row=0, column=0)

        self.new_contact = Button(self, text="New Contact", command=lambda: self.controller.show_frame(AddContactPage))
        self.new_contact.grid(row=0, column=1)

        self.settings = Button(self, text="Settings", command=lambda: self.controller.show_frame(SettingsPage))
        self.settings.grid(row=0, column=2)

        self.scroll_bar = Scrollbar(self)
        self.scroll_bar.grid(row=1, column=4, sticky=N+S+W)

        self.contacts_field = Listbox(
            self,
            yscrollcommand=self.scroll_bar.set
        )
        self.contacts_field.grid(row=1, column=0, columnspan=3, sticky=N+S+E+W)

        self.scroll_bar.config(command=self.contacts_field.yview)

    def insert_contact(self, contact):
        self.contacts_field.insert(END, contact)

    def show_contact_info(self):
        name = self.contacts_field.curselection()
        print('DEBUG', name)


class AddContactPage(Frame):
    """
    Add New Contact Page:

    === Public Attributes ===
    master: The frame containing all information on this page
    controller: Reference to the Controller Class

    * Not finished
    enter_name:*
    enter_phone_num:*
    enter_email:*
    enter_address:*
    enter_notes:*
    clear:*
    add_character:*

    contacts: Button that takes the user to the 'Contacts' page
    new_contact: Button that takes the user to the 'Add New Contact' page
    settings: Button that takes the user to the 'Settings' page

    === Methods ===
    create: Initializes objects & places them on the page
    """
    def __init__(self, master, controller):
        Frame.__init__(self, master)
        self.master = master
        self.controller = controller

        # Initialize object names
        self.contact_new = Contact('')

        self.enter_name = None
        self.enter_name_label = None
        self.enter_name_button = None

        self.enter_phone_num = None
        self.enter_phone_type = None
        self.enter_phone_num_label = None
        self.enter_phone_num_button = None

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
        self.preview = None
        self.add_to_contacts = None

        self.contacts = None
        self.new_contact = None
        self.settings = None

        # Create objects
        self.create()

    def create(self):
        self.add_to_contacts = Button(
            self,
            text="Add to Contacts",
            command=lambda: self.add_contact()
        )

        self.enter_notes = Entry(self)
        self.enter_notes_label = Label(self, text="Notes:")
        self.enter_notes_label.grid(row=5, column=0)
        self.enter_notes.grid(row=5, column=1, columnspan=3)

        self.enter_address = Entry(self)
        self.enter_address_label = Label(self, text="Address")
        self.enter_address_label.grid(row=4, column=0)
        self.enter_address.grid(row=4, column=1, columnspan=3)

        self.enter_email = Entry(self)
        self.enter_email_label = Label(self, text="Email:")
        self.enter_email_label.grid(row=3, column=0)
        self.enter_email.grid(row=3, column=1, columnspan=3)

        self.enter_phone_num = Entry(self)
        self.enter_phone_num_label = Label(self, text="Phone:")
        self.enter_phone_num_label.grid(row=2, column=0)
        self.enter_phone_num.grid(row=2, column=1, columnspan=3)

        self.enter_name = Entry(self)
        self.enter_name_label = Label(self, text="Name:")
        self.enter_name_button = Button(
            self,
            text="Add",
            command=lambda: self.contact_new.change_name(self.enter_name.get())
        )
        self.enter_name_button.grid(row=1, column=4)
        self.enter_name_label.grid(row=1, column=0)
        self.enter_name.grid(row=1, column=1, columnspan=3)

        self.contacts = Button(self, text="Contacts", command=lambda: self.controller.show_frame(ContactsPage))
        self.contacts.grid(row=0, column=0)

        self.new_contact = Button(self, text="New Contact", command=lambda: self.controller.show_frame(AddContactPage))
        self.new_contact.grid(row=0, column=1)

        self.settings = Button(self, text="Settings", command=lambda: self.controller.show_frame(SettingsPage))
        self.settings.grid(row=0, column=2)

    def add_contact(self):
        name = self.new_contact.name
        if name not in self.controller.frames[ContactsPage].contacts_list:
            self.controller.frames[ContactsPage].contacts_list[name] = self.new_contact
            self.controller.frames[ContactsPage].insert_contact(name)


class SettingsPage(Frame):
    """
        Settings Page:

        === Public Attributes ===
        master: The frame containing all information on this page
        controller: Reference to the Controller Class

        contacts: Button that takes the user to the 'Contacts' page
        new_contact: Button that takes the user to the 'Add New Contact' page
        settings: Button that takes the user to the 'Settings' page

        === Methods ===
        create: Initializes objects & places them on the page
        """
    def __init__(self, master, controller):
        Frame.__init__(self, master)
        self.master = master
        self.controller = controller

        # Initialize object names
        self.contacts = None
        self.new_contact = None
        self.settings = None

        # Create objects
        self.create()

    def create(self):
        self.contacts = Button(self, text="Contacts", command=lambda: self.controller.show_frame(ContactsPage))
        self.contacts.grid(row=0, column=0)

        self.new_contact = Button(self, text="New Contact", command=lambda: self.controller.show_frame(AddContactPage))
        self.new_contact.grid(row=0, column=1)

        self.settings = Button(self, text="Settings", command=lambda: self.controller.show_frame(SettingsPage))
        self.settings.grid(row=0, column=2)


if __name__ == "__main__":
    app = Controller()
    app.mainloop()

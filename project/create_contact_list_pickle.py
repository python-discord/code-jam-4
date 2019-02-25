from project.contact import Contact
from random import randint
import pickle
"""
This script only goal was to generate a pickle to use as base contact in the main app. It generates a list of
40 contacts. The name are setup, but the phone numbers are random and all contacts will have some information
missing (as it should be in a normal contact app).
"""


def generate_random_phone_number() -> str:
    """
    Function generates a random phone number.
    :return: Random numbers in the format ###-###-####.
    """
    phone_number = ""
    i = 0
    while i < 10:
        if i == 0:
            number_to_add = randint(1, 9)
            phone_number = phone_number + str(number_to_add)
            i += 1
            continue
        if i == 2:
            number_to_add = randint(0, 9)
            phone_number = phone_number + str(number_to_add) + "-"
            i += 1
            continue
        if i == 5:
            number_to_add = randint(0, 9)
            phone_number = phone_number + str(number_to_add) + "-"
            i += 1
            continue
        number_to_add = randint(0, 9)
        phone_number = phone_number + str(number_to_add)
        i += 1

    return phone_number


def generate_random_address() -> str:
    """
    Function generate a random address with the list of street name below.
    :return: A number from 1 to 999 followed by one of the street name in the street_name variable.
    """
    street_name = ["Main Street", "River Road", "Oak Street", "Campbell Avenue", "Elizabeth II Street", "North Road",
                   "Charles Avenue", "Wellington Street", "Nelson Street", "Hill Road", "Thompson Avenue"]
    number = randint(1,999)
    street_name = street_name[randint(0, len(street_name)-1)]
    return str(number) + " " + street_name


def generate_email_adress(input_name: str) -> str:
    """
    Function takes a name and generate an email address by replace all space in the name with dot. It uses one of
    the domain name in the domain variable randomly.
    :param input_name: The name of the person we want to generate an email address for.
    :return: The email address that was generated.
    """
    domain = ["hotmail.com", "gmail.com", "hotmail.fr", "outlook.com", "yahoo.com"]
    input_name = input_name.replace(" ", ".")
    return input_name.lower() + "@" + domain[randint(0, len(domain)-1)]


def generate_note() -> str:
    note_list = ["Cool dude!", "I don't trust this guy", "Main developer at Google!", "Nice gal", "Rude person", "BFF"]
    return note_list[randint(0, len(note_list) - 1)]


if __name__ == '__main__':
    name_list = ["Ray Allen", "Clarence Boisvert", "Katherina Burpee", "Nevada Dominguez", "Xochitl Olivas",
                 "Rubi Branscome", "Emely Ackley", "Etta Holton", "Pearl Addario", "Kimi Pelosi", "Vernita Pennel",
                 "Reyes Buhl", "Jovan Selle", "Rene Nicks", "Tonia Perrault", "Michel Guzman", "William Sirois",
                 "Carline Whitesell", "Luella Rustin", "Jewell Wakefield", "Sanora Hamdan", "Idalia Hosmer",
                 "Dorethea Wommack", "Joanne Huth", "Wayne Sippel", "Arden Lopinto", "Teena Formica", "Mary Zorn",
                 "Young Gain", "Cayla Pohlmann", "Lea Fogg", "Mack Millhouse", "Lucio Likes", "Meggan Page",
                 "Neda Plasencia", "Anissa Venturi", "Berry Furrow", "Rachell Doss", "Charlott Bledsoe",
                 "Luann Goodman"]

    contact_dictionary = {}
    for name in name_list:
        contact = Contact(name)
        # For each contact, we randomly decide if we add each of the attributes.
        if randint(0, 1):
            contact.add_address("Physical", generate_random_address())
        if randint(0, 1):
            contact.add_address("Email", generate_email_adress(contact.name))
        if randint(0, 1):
            contact.add_phone_number("Home", generate_random_phone_number())
        if randint(0, 1):
            contact.add_phone_number("Work", generate_random_phone_number())
        if randint(0, 1):
            contact.add_phone_number("Personal", generate_random_phone_number())
        if randint(0, 1):
            contact.add_note(generate_note())

        contact_dictionary[name] = contact

    # Saving the dictionary on the output pickle.
    with open("contacts_pickle", 'wb') as outfile:
        pickle.dump(contact_dictionary, outfile)
    # Loading the dictionary to see if it worked.
    with open("contacts_pickle", 'rb') as infile:
        test = pickle.load(infile)
        print(test["Ray Allen"])






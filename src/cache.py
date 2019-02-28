import aiohttp
from random import randint, choice, sample
from PIL import Image, ImageTk
import os
import io


class Cache:
    '''Class used for caching images and data about the cats.'''

    def __init__(self):
        # setting class variables for use later
        self.cats = list()
        self.session = None

        # getting the directory folder for use later when opening files
        self.dir = os.path.dirname(os.path.realpath(__file__))

    async def refill(self):
        '''Gets a cache of cat data and adds it to the self.cats list'''

        # if we haven't created a session yet, do so
        if not self.session:
            self.session = aiohttp.ClientSession()

        # Run 10 times to get 10 cats
        for i in range(10):
            # initialize a dict of cat data
            cat_data = dict()

            # randomly make jumpscares happen, but not on the first image
            if randint(1, 10) == 5 and i:
                # get a random number for an image
                image_number = randint(1, 10)
                # open and resize the image using Pillow
                im = Image.open(os.path.join(self.dir, os.path.join("res",
                                os.path.join("images", f"{image_number}.jpg"))))
                im = im.resize((self.screen_x, self.screen_y - 150), Image.NEAREST)
                # make the image a tkinter image
                image = ImageTk.PhotoImage(im)
                # update the cat data dict
                cat_data.update({"image": image})
                cat_data.update({"jumpscare": True})
            else:
                # set jumpscare to False because it isnt a jumpscare image
                cat_data.update({"jumpscare": False})

                # get a url from The Cat API
                async with self.session.get('https://api.thecatapi.com/v1/images/search') as res:
                    data = await res.json()
                    url = data[0]['url']
                # get image data from that url
                async with self.session.get(url) as res:
                    image_bytes = await res.read()
                    # open and the image in pillow
                    im = Image.open(io.BytesIO(image_bytes))
                    im = im.resize((400, 440), Image.NEAREST)
                    # make the image a tkinter image
                    image = ImageTk.PhotoImage(im)
                    # update the cat data dict
                    cat_data.update({"image": image})

                # get a random name
                async with self.session.get(
                        "https://www.pawclub.com.au/assets/js/namesTemp.json") as res:
                    data = await res.json()
                    # get a random letter for the name
                    # Note: website doesn't have any b names which is why it is left out here
                    letter = choice(list('acdefghijklmnopqrstuvwxyz'))
                    # randomly choose a name from the json with that letter
                    cat = choice(data[letter])
                    # update the cat data dict
                    cat_data.update({"name": cat["name"]})
                    cat_data.update({"gender": cat["gender"]})

                # get 5 random hobbies
                async with self.session.get(
                    "https://gist.githubusercontent.com/mbejda/" +
                    "453fdb77ef8d4d3b3a67/raw/e8334f09109dc212892406e25fdee03efdc23f56/" +
                    "hobbies.txt"
                ) as res:
                    text = await res.text()
                    # split the raw text of hobbies into a list
                    all_hobbies = text.split("\n")
                    # get 5 of those hobbies
                    hobby_list = sample(all_hobbies, 5)
                    # join those 5 hobbies into a bulleted list (string)
                    list_of_hobbies = "\n •".join(hobby_list)
                    hobbies = f"Hobbies:\n •{list_of_hobbies}"
                    # update the cat_data dict
                    cat_data.update({"hobbies": hobbies})

                # get a random age between 1 and 15 (avg lifespan of a cat)
                age = str(randint(1, 15))
                # update the cat data dict
                cat_data.update({"age": age})

                # get a random number of miles away between 1 and 5
                miles = randint(1, 5)
                location = f"{miles} miles away"
                # update the cat data dict
                cat_data.update({"location": location})
            self.cats.append(cat_data)

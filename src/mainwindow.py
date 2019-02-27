import tkinter as tk
from PIL import Image, ImageTk
import io
from random import randint, choice, sample
import asyncio
import aiohttp
import os
from pygame import mixer


class Tinder:
    def __init__(self):
        # setup for pygame mixer
        mixer.init()

        # getting the directory folder for use later when opening files
        self.dir = os.path.dirname(os.path.realpath(__file__))

        # setting up the tkinter root
        self.root = tk.Tk()
        self.root.title("Cat Tinder")
        self.root.geometry("400x500")
        self.root.minsize(400, 500)
        self.root.maxsize(400, 500)
        self.root.configure(background='black')
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # getting screen width and height for use with teleporting window/jumpscare
        self.screen_x = self.root.winfo_screenwidth()
        self.screen_y = self.root.winfo_screenheight()

        # setting class variables to be used later
        self.jumpscare = False
        self.loop = asyncio.get_event_loop()
        self.session = None
        self.cats = list()

    def start(self):
        '''Starts the Tinder application'''

        # getting a cache of cat info
        self.loop.run_until_complete(self.get_cache())

        # starting the program loop
        self.new_image()

    async def get_cache(self):
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

    def all_children(self):
        '''Used to get all children of the root window

        Returns
        -------
            A `list` of tkinter objects that are children of the root window'''

        # get children
        children = self.root.winfo_children()
        # loop through the children
        for item in children:
            # if the child has children, add them to the list
            if item.winfo_children():
                children.extend(item.winfo_children())
        # return the full list of children
        return children

    def new_image(self, cat=None):
        '''Main functionality of the application

        param
            cat: dict -- if you want to run the function without getting a new cat'''

        # if the previous image was a jumpscare, resize the window and reset the variable
        if self.jumpscare:
            self.root.maxsize(400, 500)
            self.jumpscare = False

        # get all children of the root window
        widget_list = self.all_children()
        for item in widget_list:
            # forget packs all of the children (This clears the window)
            item.pack_forget()

        # make a new Frame
        self.frame = tk.Frame(self.root, bg="black")

        # if a dict wasn't passed to the function, get a dict from self.cats
        if not cat:
            try:
                cat = self.cats.pop(0)
            except IndexError:
                # the cache is empty so refill it
                self.loop.run_until_complete(self.get_cache())
                cat = self.cats.pop(0)

        # getting cat variables from the dict
        cat_name = cat["name"]
        image = cat["image"]
        jumpscare = cat["jumpscare"]
        gender = cat["gender"].capitalize()
        hobbies = cat["hobbies"]
        age = cat["age"]
        location = cat["location"]

        # if the image is not a jumpscare, add a Text widget with the cat name
        if not jumpscare:
            # make the Text widget
            name = tk.Text(self.frame, width=40, height=1)
            # tag to make all text in the widget centered
            name.tag_configure("center", justify=tk.CENTER)
            # insert the cat name into the widget
            name.insert("1.0", cat_name)
            # add the centered tag to all text in the widget
            name.tag_add("center", "1.0", tk.END)
            # disable the widget so the user can't type in it
            name.configure(state="disabled")
            # pack the widget on the top of the frame
            name.pack(side=tk.TOP)

        # make a Label widget with the cat/jumpscare image and pack it
        tk.Label(self.frame, image=image).pack(side=tk.TOP)

        # the image is a jumpscare, so do jumpscare things
        if jumpscare:
            # remember that this image is a jumpscare
            self.jumpscare = True

            # allow the root window to get bigger
            self.root.maxsize(self.screen_x, self.screen_y)
            # make the root window bigger (makes jumpscare image scarier)
            self.root.geometry(f"{self.screen_x}x{self.screen_y}+0+0")

            # play a jumpscare sound
            mixer.music.load(
                os.path.join(self.dir, os.path.join(
                    "res", os.path.join("sounds", "jumpscare.mp3"))
                    )
                )
            mixer.music.play()

            # make a button to allow the user to pass through the image
            # Note: since everyone likes scary monsters, only make a Like button
            tk.Button(
                self.frame, text="Like", background="green", command=self.new_image
                ).pack(side=tk.BOTTOM)

        # image was not a jumpscare, don't do jumpscare things
        else:
            # setting up like and dislike buttons on opposite sides of the screen
            tk.Button(
                self.frame, text="Like", background="green", command=self.new_image
                ).pack(side=tk.RIGHT)
            tk.Button(
                self.frame, text="Dislike", background="red", command=self.new_image
                ).pack(side=tk.LEFT)

            # defining button functions
            def back_to_photo():
                '''Resets the window with the same cat for when the user
                goes to bio and clicks back'''

                # calls the new image function and passes the current cat dict
                self.new_image(cat)

            def get_bio():
                '''Creates the Bio Widget for the current cat'''

                # get all children of the root window
                widget_list = self.all_children()
                for item in widget_list:
                    # forget packs all of the children (This clears the window)
                    item.pack_forget()

                # make a new Frame for the bio
                self.frame = tk.Frame(self.root, bg="black", height=450, width=400)

                # makes a Text widget on the Frame
                bio = tk.Text(self.frame)

                # inserting all of the Bio to the text widget
                bio.insert(tk.END, f"Name: {cat_name} \n")
                bio.insert(tk.END, f"Age: {age} \n")
                bio.insert(tk.END, f"Gender: {gender} \n")
                bio.insert(tk.END, f"Location: {location} \n")
                bio.insert(tk.END, f"{hobbies} \n")
                # disabling the widget so users can't edit it
                bio.configure(state="disabled")
                # packing the bio
                bio.pack(side=tk.TOP)

                # setting up like/dislike/Back to Photo buttons on the bio screen
                tk.Button(
                    self.frame, text="Like", background="green", command=self.new_image
                    ).pack(side=tk.RIGHT)
                tk.Button(
                    self.frame, text="Dislike", background="red", command=self.new_image
                    ).pack(side=tk.LEFT)
                tk.Button(
                    self.root, text="Back To Photo", background="blue", command=back_to_photo
                    ).pack(side=tk.BOTTOM)

                # packing the frame
                self.frame.pack()

            # making and packing the Bio button for users to look at the cat's bio
            tk.Button(
                self.frame, text="Bio", background="blue", command=get_bio
                ).pack(side=tk.BOTTOM)

        # packing the frame
        self.frame.pack()

        # starting the main tkinter loop
        self.root.mainloop()

    def on_closing(self):
        '''Teleports the window if the user tries to close the app using the red X'''

        # checks if the image is a jumpscare (if so, can't teleport the
        # window because it takes up the entire screen)
        if not self.jumpscare:
            # get the max x and y values that the window can teleport
            # to without going off the screen
            max_x, max_y = self.screen_x - 400, self.screen_y - 500
            # getting the random x and y values to teleport to
            x, y = randint(0, max_x), randint(0, max_y)
            # moving the window to those x and y coordinates
            self.root.geometry(f"+{x}+{y}")


# checks if this file is the main file being run
if __name__ == "__main__":
    # start the application
    Tinder().start()

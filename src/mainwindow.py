import configparser
import tkinter as tk
import asyncio
from pygame import mixer
from .cache import Cache
from .animate import Animater, Coord

from . import SETTINGS


class Tinder:
    '''The main class for the application.'''

    def __init__(self):
        # setup for pygame mixer
        mixer.init()

        # get settings
        cp = configparser.ConfigParser()
        cp.read(SETTINGS)

        # for now, let's just look up the DEV settings
        # can change this later
        # configparser will use values from DEFAULT section if none provided elsewhere
        if 'DEV' in cp.sections():
            self.config = cp['DEV']
        else:
            self.config = cp['DEFAULT']

        # setting up the tkinter root
        self.root = tk.Tk()
        self.root.title(self.config['main.title'])
        self.root.geometry(self.config['main.geometry'])
        self.root.minsize(400, 500)
        self.root.maxsize(400, 500)
        self.root.configure(background=self.config['main.background'])
        # self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # getting screen width and height for use with teleporting window/jumpscare
        self.screen_x = self.root.winfo_screenwidth()
        self.screen_y = self.root.winfo_screenheight()

        # setting class variables to be used later
        self.jumpscare = False
        self.loop = asyncio.get_event_loop()
        self.cache = Cache(self.root)

    def start(self):
        '''Starts the Tinder application'''

        # getting a cache of cat info
        self.loop.run_until_complete(self.cache.refill())

        # starting the program loop
        self.new_image()

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
                cat = self.cache.cats.pop(0)
            except IndexError:
                # the cache is empty so refill it
                self.loop.run_until_complete(self.cache.refill())
                cat = self.cache.cats.pop(0)

        # getting base cat variables from the dict
        image = cat["image"]
        jumpscare = cat["jumpscare"]

        # if the image is not a jumpscare, add a Text widget with the cat name
        if not jumpscare:
            # since the image is not a jumpscare, get regular cat variables
            cat_name = cat["name"]
            gender = cat["gender"].capitalize()
            hobbies = cat["hobbies"]
            age = cat["age"]
            location = cat["location"]

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
            soundpath = SOUNDS / "jumpscare.mp3"
            mixer.music.load(str(soundpath))
            mixer.music.play()

            # make a button to allow the user to pass through the image
            # Note: since everyone likes scary monsters, only make a Like button
            tk.Button(
                self.frame, text=self.config['like.text'], background="green",
                command=self.new_image).pack(side=tk.BOTTOM)

        # image was not a jumpscare, don't do jumpscare things
        else:
            # setting up like and dislike buttons on opposite sides of the screen
            tk.Button(
                self.frame, text=self.config['like.text'], background="green",
                command=self.new_image).pack(side=tk.RIGHT)
            tk.Button(
                self.frame, text=self.config['dislike.text'], background="red",
                command=self.new_image).pack(side=tk.LEFT)

            # defining button functions
            def back_to_photo():
                '''Resets the window with the same cat for when the user
                goes to bio and clicks back'''

                # calls the new image function and passes the current cat dict
                self.window.clear()
                self.window.add_motion(self.bioid, (Coord(0, 500),), speed=3)
                self.window.start()
                self.new_image(cat)

            def get_bio():
                '''Creates the Bio Widget for the current cat'''

                # get all children of the root window
                widget_list = self.all_children()
                for item in widget_list:
                    # forget packs all of the children (This clears the window)
                    item.pack_forget()

                # make a new Frame for the bio
                self.window = Animater(self.root)
                self.frame = tk.Frame(self.window, bg="black", height=450, width=400)

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
                    self.frame, text=self.config['like.text'],
                    background=self.config['like.background'],
                    command=self.new_image).pack(side=tk.RIGHT)
                tk.Button(
                    self.frame, text=self.config['dislike.text'],
                    background=self.config['dislike.background'],
                    command=self.new_image).pack(side=tk.LEFT)
                tk.Button(
                    self.root, text=self.config['back.text'],
                    background=self.config['back.background'],
                    command=back_to_photo).pack(side=tk.BOTTOM)

                # packing the frame
                self.bioid = self.window.create_window((0, 500), window=self.frame, anchor='nw')
                end = Coord(0, 0)
                self.window.add_motion(self.bioid, (end,), speed=3)
                self.window.pack(fill='both', expand=True)
                self.window.start()

            # making and packing the Bio button for users to look at the cat's bio
            tk.Button(
                self.frame, text=self.config['bio.text'], background=self.config['bio.background'],
                command=get_bio).pack(side=tk.BOTTOM)

        # packing the frame
        self.frame.pack()

        # starting the main tkinter loop
        self.root.mainloop()

    def on_closing(self):
        '''Teleports the window if the user tries to close the app using the red X'''

        # checks if the image is a jumpscare (if so, can't teleport the
        # window because it takes up the entire screen)
        return
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

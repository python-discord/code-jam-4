import tkinter as tk
from PIL import Image, ImageTk
import io
from random import randint, choice
import asyncio
import time
import aiohttp
import os
from pygame import mixer


class Tinder:
    def __init__(self):
        mixer.init()
        self.dir = os.path.dirname(os.path.realpath(__file__))
        self.root = tk.Tk()
        self.root.title("Cat Tinder")
        self.root.geometry("400x500")
        self.root.configure(background='grey')
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        #self.root.bind('<Motion>', self.motion)
        self.loop = asyncio.get_event_loop()
        self.session = None
        self.images = list()
        
        
    def start(self):
        self.loop.run_until_complete(self.get_cache())
        self.new_image()


    async def get_cache(self):
        print("refreshing image cache")
        t = time.time()
        if not self.session:
            self.session = aiohttp.ClientSession()
        for _ in range(10):
            if randint(0,9) == 9:
                image_number = randint(1,10)
                im = Image.open(os.path.join(self.dir, os.path.join("res", os.path.join("images", f"{image_number}.jpg"))))
                im = im.resize((400, 400), Image.NEAREST)
                image = ImageTk.PhotoImage(im)
                async with self.session.get("https://www.pawclub.com.au/assets/js/namesTemp.json") as res:
                    data = await res.json()
                    names = choice(data["a"])
                    name = names["name"]
                self.images.append([image, True, name])
            else:
                async with self.session.get('https://api.thecatapi.com/v1/images/search') as res:
                    data = await res.json()
                    url = data[0]['url']
                async with self.session.get(url) as res:
                    image_bytes = await res.read()
                    im = Image.open(io.BytesIO(image_bytes))
                    im = im.resize((400, 400), Image.NEAREST)
                    image = ImageTk.PhotoImage(im)
                async with self.session.get("https://www.pawclub.com.au/assets/js/namesTemp.json") as res:
                    data = await res.json()
                    letter = choice(list('acdefghijklmnopqrstuvwxyz'))
                    names = choice(data[letter])
                    name = names["name"]
                self.images.append([image, False, name])
        print(time.time()-t)


    async def get_bio(self):
        #code to get bio goes here
        #probably want to return a dict of some sort
        pass


    def bio(self):
        self.loop.run_until_complete(self.get_bio())


    def all_children(self):
        children = self.root.winfo_children()
        for item in children:
            if item.winfo_children():
                children.extend(item.winfo_children())
        return children


    def new_image(self):
        widget_list = self.all_children()
        for item in widget_list:
            item.pack_forget()
        self.frame = tk.Frame(self.root, bg = "black")
        try:
            image, jumpscare, cat_name = self.images.pop(0)
        except IndexError:
            self.loop.run_until_complete(self.get_cache())
            image, jumpscare, cat_name = self.images.pop(0)
        name = tk.Text(self.frame, width = 40, height = 1)
        name.tag_configure("center", justify=tk.CENTER)
        name.insert("1.0", cat_name)
        name.tag_add("center", "1.0", tk.END)
        name.configure(state="disabled")
        name.pack(side = tk.TOP)
        tk.Label(self.frame, image=image).pack(side = tk.TOP)
        tk.Button(self.frame, text="Like", background="green", command = self.new_image).pack(side = tk.RIGHT)
        tk.Button(self.frame, text="Dislike", background="red", command = self.new_image).pack(side = tk.LEFT)
        def get_bio():
            widget_list = self.all_children()
            for item in widget_list:
                item.pack_forget()
            self.frame = tk.Frame(self.root, bg = "black")
            full_bio = self.loop.run_until_complete(self.get_bio())
            bio = tk.Text(self.frame)
        tk.Button(self.frame, text="Bio", background="blue", command = get_bio).pack(side = tk.BOTTOM)
        if jumpscare:
            mixer.music.load(os.path.join(self.dir, os.path.join("res", os.path.join("sounds", "jumpscare.mp3"))))
            mixer.music.play()
        self.frame.pack()
        self.root.mainloop()


    def on_closing(self):
        x = randint(0, 1520)
        y = randint(0, 580)
        self.root.geometry(f"+{x}+{y}")


    def motion(self,event):
        frame_x, frame_y = self.frame.winfo_x(), self.frame.winfo_y()
        x, y = event.x, event.y
        if x > 300 and y < 15:
            move_x = (400 - x) + frame_x
            move_y = (15 - y) - frame_y
            self.root.geometry(f"400x500+{move_x}+{move_y}")


if __name__ == "__main__":
    Tinder().start()
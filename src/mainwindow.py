import tkinter as tk
from PIL import Image, ImageTk
import io
from random import randint, choice, sample
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
            cat_data = dict()
            if randint(0,9) == 9:
                image_number = randint(1,10)
                im = Image.open(os.path.join(self.dir, os.path.join("res", os.path.join("images", f"{image_number}.jpg"))))
                im = im.resize((400, 400), Image.NEAREST)
                image = ImageTk.PhotoImage(im)
                cat_data.update({"image" : image})
                cat_data.update({"jumpscare": True})
            else:
                cat_data.update({"jumpscare": False})
                async with self.session.get('https://api.thecatapi.com/v1/images/search') as res:
                    data = await res.json()
                    url = data[0]['url']
                async with self.session.get(url) as res:
                    image_bytes = await res.read()
                    im = Image.open(io.BytesIO(image_bytes))
                    im = im.resize((400, 450), Image.NEAREST)
                    image = ImageTk.PhotoImage(im)
                    cat_data.update({"image":image})
            async with self.session.get("https://www.pawclub.com.au/assets/js/namesTemp.json") as res:
                data = await res.json()
                letter = choice(list('acdefghijklmnopqrstuvwxyz'))
                cat = choice(data[letter])
                cat_data.update({"name":cat["name"]})
                cat_data.update({"gender":cat["gender"]})    
            async with self.session.get("https://gist.githubusercontent.com/mbejda/453fdb77ef8d4d3b3a67/raw/e8334f09109dc212892406e25fdee03efdc23f56/hobbies.txt") as res:
                text = await res.text()
                all_hobbies = text.split("\n") 
                hobby_list = sample(all_hobbies, 5)
                list_of_hobbies = "\n •".join(hobby_list)
                hobbies = f"Hobbies:\n •{list_of_hobbies}" 
                cat_data.update({"hobbies":hobbies})
            age = str(randint(1,15))
            cat_data.update({"age":age})   
            miles = randint(1,5)
            location = f"{miles} miles away"
            cat_data.update({"location":location})
            self.images.append(cat_data)
        print(time.time()-t)


    def all_children(self):
        children = self.root.winfo_children()
        for item in children:
            if item.winfo_children():
                children.extend(item.winfo_children())
        return children


    def new_image(self, cat= None):
        widget_list = self.all_children()
        for item in widget_list:
            item.pack_forget()
        self.frame = tk.Frame(self.root, bg = "black")
        if not cat:
            try:
                cat = self.images.pop(0)
            except IndexError:
                self.loop.run_until_complete(self.get_cache())
                cat = self.images.pop(0)
        cat_name = cat["name"]
        image = cat["image"]
        jumpscare = cat["jumpscare"]
        gender = cat["gender"].capitalize()
        hobbies = cat["hobbies"]
        age = cat["age"]
        location = cat["location"]
        if not jumpscare:
            name = tk.Text(self.frame, width = 40, height = 1)
            name.tag_configure("center", justify=tk.CENTER)
            name.insert("1.0", cat_name)
            name.tag_add("center", "1.0", tk.END)
            name.configure(state="disabled")
            name.pack(side = tk.TOP)
        tk.Label(self.frame, image=image).pack(side = tk.TOP)
        if jumpscare:
            mixer.music.load(os.path.join(self.dir, os.path.join("res", os.path.join("sounds", "jumpscare.mp3"))))
            mixer.music.play()
            tk.Button(self.frame, text="Like", background="green", command = self.new_image).pack(side = tk.BOTTOM)
        else:
            tk.Button(self.frame, text="Like", background="green", command = self.new_image).pack(side = tk.RIGHT)
            tk.Button(self.frame, text="Dislike", background="red", command = self.new_image).pack(side = tk.LEFT)
            def back_to_photo():
                self.new_image(cat)
            def get_bio():
                widget_list = self.all_children()
                for item in widget_list:
                    item.pack_forget()
                self.frame = tk.Frame(self.root, bg = "black")
                bio = tk.Text(self.frame)
                bio.insert(tk.END, f"Name: {cat_name} \n")
                bio.insert(tk.END, f"Age: {age} \n")
                bio.insert(tk.END, f"Gender: {gender} \n")
                bio.insert(tk.END, f"Location: {location} \n")
                bio.insert(tk.END, f"{hobbies} \n")                
                bio.configure(state="disabled")
                bio.pack(side = tk.TOP)
                tk.Button(self.frame, text="Back To Photo", background="blue", command = back_to_photo).pack(side = tk.BOTTOM)
                self.frame.pack()
            tk.Button(self.frame, text="Bio", background="blue", command = get_bio).pack(side = tk.BOTTOM)
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

import requests
import time
# import configparser

from random import randint, choice, sample
from multiprocessing import Process, Queue

# from . import SETTINGS, IMAGES


class ImageCache:
    '''Class used for caching images'''
    image_api = 'https://api.thecatapi.com/v1/images/search'
    profile_api = "https://www.pawclub.com.au/assets/js/namesTemp.json"
    hobbies_api = (
        "https://gist.githubusercontent.com/mbejda/453fdb77ef8d4d3b3a67/raw/"
        "e8334f09109dc212892406e25fdee03efdc23f56/hobbies.txt"
    )
    ratelimit = 0.1

    def __init__(self, master, cachesize):
        self.master = master
        self.cachesize = cachesize
        self.screen_x = self.master.winfo_screenwidth()
        self.screen_y = self.master.winfo_screenheight()

        self.queue = Queue(self.cachesize)
        self.active = False
        self.worker = None

    def __del__(self):
        self.stop()

    def get_image(self):
        res = requests.get(self.image_api, stream=True)
        data = res.json()
        url = data[0]['url']
        res = requests.get(url)
        return res.content

    def get_hobbies(self):
        res = requests.get(self.hobbies_api)
        all_hobbies = res.text.split("\n")
        return sample(all_hobbies, 5)

    def get_profile(self):
        res = requests.get(self.profile_api)
        data = res.json()
        letter = choice('acdefghijklmnopqrstuvwxyz')
        data = choice(data[letter])
        return {
            'name': data['name'],
            'gender': data['gender'],
            'age': randint(1, 42),
            'location': f'{randint(1, 9999)} miles away',
            'image': self.get_image(),
            'hobbies': self.get_hobbies()
        }

    def next(self):
        return self.queue.get()

    def mainloop(self, queue):
        while True:
            if not queue.full():
                queue.put(self.get_profile())
        time.sleep(self.ratelimit)

    def start(self):
        if self.worker is not None and self.worker.is_alive():
            self.stop()
        self.active = True
        self.worker = Process(target=self.mainloop, args=(self.queue,))
        self.worker.start()

    def stop(self):
        self.active = False
        self.worker.join()

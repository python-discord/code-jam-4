import json
import requests
import time
import multiprocessing as mp
from random import randint, choice, sample

from . import API


class ImageCache:
    '''Class used for caching images'''

    ratelimit = 0.05
    with API.open() as fp:
        api = json.load(fp)

    def __init__(self, size):
        self.manager = mp.Manager()
        self.queue = self.manager.Queue(size)
        self.worker = None

        self.infocache = None
        self.hobbycache = None

    def __del__(self):
        self.stop()

    def __get(self, url, **kwargs):
        try:
            return requests.get(url, **kwargs)
        except ConnectionError as e:
            return e

    def __parse_image(self, data: dict):
        data = response.json()
        url = data[0]['url']
        response = self.__get(url)
        return {'image': response.content}

    def __parse_hobbies(self, response):
        all_hobbies = response.text.split("\n")
        return {'hobbies': sample(all_hobbies, 5)}

    def __parse_info(self, response):
        data = response.json()
        letter = choice('acdefghijklmnopqrstuvwxyz')
        data = choice(data[letter])
        return {
            'info': {
                'name': data['name'],
                'gender': data['gender'],
                'age': randint(1, 42),
                'location': f'{randint(1, 9999)} miles away'
            }
        }

    def get_profile(self):
        api = [self.api['image']]
        if self.infocache is None:
            api.append(self.api['info'])
        if self.

        with mp.Pool(poolsize) as pool:
            response = pool.map(self.__get, self.api.values())
        if ConnectionError not in responses:  # TODO Record connection errors
            return {
                **self.__parse_info(response['info']),
                **self.__parse_image(response['image']),
                **self.__parse_hobbies(response['hobbies'])
            }

    def next(self):
        return self.queue.get()

    def mainloop(self, queue):
        while True:
            profile = self.get_profile()
            if profile is not None:
                queue.put(profile)
            time.sleep(self.ratelimit)

    def start(self):
        if self.worker is not None and self.worker.is_alive():
            self.stop()
        self.worker = mp.Process(target=self.mainloop, args=(self.queue,))
        self.worker.start()

    def stop(self):
        for worker in mp.active_children():
            worker.terminate()

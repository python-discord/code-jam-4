import json
import requests
import time
import multiprocessing as mp

from typing import List, Text
from random import randint, choice, sample

from . import API


class ImageCache:
    """Class used for caching images"""

    ratelimit = 0.05
    with API.open() as fp:
        api = json.load(fp)

    api_cache = {
        'info': None,
        'hobbies': None
    }

    def __init__(self, size):
        self.queue = mp.Queue(size)
        self.worker = None

    def __del__(self):
        self.stop()

    def __get(self, url, **kwargs):
        try:
            return requests.get(url, **kwargs)
        except ConnectionError as e:
            return e

    def __parse_image(self, data: List[dict]) -> dict:
        url = data[0]['url']
        response = self.__get(url)
        return {'image': response.content}

    def __parse_hobbies(self, data: Text):
        return {'hobbies': sample(data, 5)}

    def __parse_info(self, data: dict):
        letter = choice('acdefghijklmnopqrstuvwxyz')
        data = choice(data[letter])
        return {
            'name': data['name'],
            'info': {
                'gender': data['gender'],
                'age': randint(1, 42),
                'location': f'{randint(1, 9999)} miles away'
            }
        }

    def get_profile(self):
        response = {k: self.__get(v) for k, v in self.api.items() if self.api_cache.get(k) is None}
        if ConnectionError not in response:  # TODO Record connection errors
            if 'info' in response:
                self.api_cache['info'] = response['info'].json()
            if 'hobbies' in response:
                self.api_cache['hobbies'] = response['hobbies'].text.split('\n')
            return {
                **self.__parse_info(self.api_cache['info']),
                **self.__parse_hobbies(self.api_cache['hobbies']),
                **self.__parse_image(response['image'].json())
            }

    def mainloop(self, queue):
        while True:
            profile = self.get_profile()
            if profile is not None:
                queue.put(profile)
            time.sleep(self.ratelimit)

    def next(self):
        return self.queue.get()

    def start(self):
        if self.worker is not None and self.worker.is_alive():
            self.stop()
        self.worker = mp.Process(target=self.mainloop, args=(self.queue,))
        self.worker.start()

    def stop(self):
        self.worker.terminate()

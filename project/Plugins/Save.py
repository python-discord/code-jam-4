""" Contains logic for loading and saving states """
import json
from project.utils import CONSTANTS


def getQuotes():
    # due to some more complex characters in 'app.json' the encoding must be set utf-8
    with open(CONSTANTS['APP_SETTINGS'], encoding='utf-8') as f:
        data = json.load(f)
        return data['quotes']

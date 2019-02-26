import os
import configparser

config_file = 'notepad.ini'
app_config = configparser.ConfigParser()  # import this to other modules for access to configuration


def create_default_config(config):
    config['License'] = {}
    config['License']['eulaaccepted'] = 'no'


try:
    with open(config_file) as f:
        app_config.read(f)
except FileNotFoundError:
    create_default_config(app_config)
    with open(config_file, 'w') as f:
        app_config.write(f)

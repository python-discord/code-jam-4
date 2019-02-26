import os
import configparser

config_file = 'notepad.ini'
app_config = configparser.ConfigParser()  # import this to other modules for access to configuration


def create_default_config(config):
    config['License'] = {}
    config['License']['eulaaccepted'] = 'no'


if os.path.exists(config_file):
    app_config.read(config_file)
else:
    create_default_config(app_config)
    with open(config_file, 'w') as f:
        app_config.write(f)

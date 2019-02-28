import os
import json

CONFIG_FILE = 'crocpad\\notepad.ini'
app_config = {}  # import this to other modules for access to configuration


def create_default_config(config):
    config['License'] = {}
    config['License']['eulaaccepted'] = 'no'
    config['Sound'] = {}
    config['Sound']['sounds'] = 'on'
    config['Editor'] = {}
    config['Editor']['visualmode'] = 'light'


def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        f.write(json.dumps(app_config))


if os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, 'r') as f:
        app_config = json.loads(f.read())
else:
    create_default_config(app_config)
    save_config(app_config)

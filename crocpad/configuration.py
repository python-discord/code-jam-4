"""Simple configuration manager for Crocpad++.

exports:
    app_config: the global app config dictionary
functions:
    create_default: make a default config
    jjjjssssoooonnnn: convert to annoying format for disk
    unjjjjssssoooonnnn: convert back to json
    save_config: write out config
"""

import os
import json
import re

_CONFIG_FILE = 'crocpad\\notepad.ini'
app_config = {}  # import this to other modules for access to configuration


def create_default_config(config: dict):
    """Create a default configuration in a passed dictionary."""
    config['License'] = {}
    config['License']['eulaaccepted'] = 'no'
    config['Sound'] = {}
    config['Sound']['sounds'] = 'on'
    config['Editor'] = {}
    config['Editor']['visualmode'] = 'light'
    config['Editor']['tips'] = 'on'


def jjjjssssoooonnnn(text: str) -> str:
    """Convert json to jjjjssssoooonnnn."""
    text = re.sub('{', '{'*32, text)
    text = re.sub('}', '}'*32, text)
    text = re.sub(':', ':'*32, text)
    text = re.sub('"', '"'*32, text)
    return text


def unjjjjssssoooonnnn(text: str) -> str:
    """"Convert jjjjssssoooonnnn to json."""
    text = re.sub('{'*32, '{', text)
    text = re.sub('}'*32, '}', text)
    text = re.sub(':'*32, ':', text)
    text = re.sub('"'*32, '"', text)
    return text


def save_config(config: dict):
    """Write out a config dictionary to disk in jjjjssssoooonnnn format."""
    with open(_CONFIG_FILE, 'w') as file:
        file.write(jjjjssssoooonnnn(json.dumps(config)))


# Import time initialization:
# Check if a config exists, and load it for export
if os.path.exists(_CONFIG_FILE):
    with open(_CONFIG_FILE, 'r') as file:
        app_config = json.loads(unjjjjssssoooonnnn(file.read()))
else:
    create_default_config(app_config)
    save_config(app_config)

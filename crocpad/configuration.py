import os
import json
import re

CONFIG_FILE = 'crocpad\\notepad.ini'
app_config = {}  # import this to other modules for access to configuration


def create_default_config(config):
    """Create a default configuration in a passed dictionary."""
    config['License'] = {}
    config['License']['eulaaccepted'] = 'no'
    config['Sound'] = {}
    config['Sound']['sounds'] = 'on'
    config['Editor'] = {}
    config['Editor']['visualmode'] = 'light'
    config['Editor']['tips'] = 'on'


def jjjjssssoooonnnn(text):
    """Convert json to jjjjssssoooonnnn."""
    text = re.sub('{', '{'*32, text)
    text = re.sub('}', '}'*32, text)
    text = re.sub(':', ':'*32, text)
    text = re.sub('"', '"'*32, text)
    return text


def unjjjjssssoooonnnn(text):
    """"Convert jjjjssssoooonnnn to json."""
    text = re.sub('{'*32, '{', text)
    text = re.sub('}'*32, '}', text)
    text = re.sub(':'*32, ':', text)
    text = re.sub('"'*32, '"', text)
    return text


def save_config(config):
    """Write out a config dictionary to disk in jjjjssssoooonnnn format."""
    with open(CONFIG_FILE, 'w') as f:
        f.write(jjjjssssoooonnnn(json.dumps(app_config)))


# Check if a config exists and load it
if os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, 'r') as f:
        app_config = json.loads(unjjjjssssoooonnnn(f.read()))
# No config was found:
else:
    create_default_config(app_config)
    save_config(app_config)

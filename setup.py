import urllib.request as r
from os import makedirs
from os.path import realpath, dirname

#
# Downloading the file with the city names
#
project_root = dirname(realpath(__file__))
data_directory = project_root + '/data/'
filename = 'world-cities.csv'

makedirs(data_directory, exist_ok=True)

data_urls = {"world-cities.csv": "https://pkgstore.datahub.io/core/"
             "world-cities/world-cities_csv/"
             "data/6cc66692f0e82b18216a48443b6b95da"
             "/world-cities_csv.csv",
             "gear.png": "https://i.imgur.com/LLbDEiD.png",
             "glass.png": "https://i.imgur.com/UUKK41O.png"}

for filename, url in data_urls.items():
    r.urlretrieve(url, data_directory + filename)

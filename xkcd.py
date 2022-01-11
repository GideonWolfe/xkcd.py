import argparse
import colorsys
import json
import requests
import os
import random
import urllib.request
import subprocess


# Set up command line options
parser = argparse.ArgumentParser(description='Generate XKCD wallpapers.')
parser.add_argument('-b', '--bgcolor', default="#EAD494", dest='bgcolor', action='store', help='color value in hex notation')
parser.add_argument('-n', '--comicnum', default="random", dest='comicnum', action='store', help='which comic to use')
args = parser.parse_args()


# Returns the number of the latest comic
def get_max_comic_num():
    # Grab the info about latest comic and load it into JSON
    data = requests.get("https://xkcd.com/info.0.json")
    jsonData = json.loads(data.text)

    return int(jsonData['num'])

# returns the URL of a comic between 1 and max
def get_comic(comicnum):
    infoURL = "https://xkcd.com/{cnum}/info.0.json".format(cnum=comicnum)
    data = requests.get(infoURL)
    jsonData = json.loads(data.text)
    imageURL = jsonData['img']
    return imageURL
    
# returns the URL of a random comic between 1 and max
def get_random_comic():
    maxcomic = get_max_comic_num()
    randomcomic = random.randrange(maxcomic)
    infoURL = "https://xkcd.com/{cnum}/info.0.json".format(cnum=randomcomic)
    data = requests.get(infoURL)
    jsonData = json.loads(data.text)
    imageURL = jsonData['img']
    return imageURL

def setup_cache_dir():
    homedir = os.path.expanduser("~") # without the ending /
    cachedir = homedir+"/.cache/xkcd"
    if os.path.isdir(cachedir):
        print("Cache directory found... Continuing")
        return(cachedir)
    else:
        print("No cache directory found... Creating")
        os.mkdir(cachedir)
        return(cachedir)

# Takes an image URL and saves it to $HOME/.cache/xkcd/comic.ext
def download_image(url, cacheDir):
    full_path = cacheDir + "/comic.png"
    urllib.request.urlretrieve(url, full_path)

def add_drop_shadow():
    source_path = setup_cache_dir() + "/comic.png"
    target_path = setup_cache_dir() + "/shadowcomic.png"
    args = ["convert", source_path, "(", "-clone", "0", "-background", "gray", "-shadow", "80x3+10+10", ")", "-reverse", "-background", "none", "-layers", "merge", "+repage", target_path]
    subprocess.run(args, capture_output=True)

def add_background():
    source_path = setup_cache_dir() + "/shadowcomic.png"
    target_path = setup_cache_dir() + "/background.png"
    args = ["convert", source_path, "-gravity", "center", "-background", "blue", "-extent", "1920x1080", target_path]
    subprocess.run(args, capture_output=True)


def main():
    # Setup
    #  setup_cache_dir()

    #  url = get_random_comic()

    #  download_image(url, setup_cache_dir())

    #  add_drop_shadow()
    add_background()



main()

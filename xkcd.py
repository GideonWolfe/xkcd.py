import argparse
import colorsys
import json
import requests
import os
import random
import urllib.request
import subprocess
import colorsys



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


def add_background(bgcolor):
    source_path = setup_cache_dir() + "/shadowcomic.png"
    target_path = setup_cache_dir() + "/background.png"
    cmdargs = ["convert", source_path, "-gravity", "center", "-background", bgcolor, "-extent", "1920x1080", target_path]
    subprocess.run(cmdargs, capture_output=True)

def generate_shadow_color(bgcolor):
    rawHex = bgcolor.lstrip("#")
    rgb = tuple(int(rawHex[i:i+2], 16) for i in (0, 2, 4))
    print(rgb)
    colorList = list(rgb)
    for i in range(0, len(colorList)):
        colorList[i] = int(colorList[i]*0.8)
    rgb = tuple(colorList)
    #  hsv = colorsys.rgb_to_hsv(*rgb)
    #  print(hsv)
    print(rgb)
    return(rgb)

def add_drop_shadow(bgcolor):
    shadow_color = list(generate_shadow_color(bgcolor))
    color_string = "rgb({},{},{})".format(shadow_color[0], shadow_color[1], shadow_color[2])
    source_path = setup_cache_dir() + "/comic.png"
    target_path = setup_cache_dir() + "/shadowcomic.png"
    #  args = ["convert", source_path, "(", "-clone", "0", "-background", "gray", "-shadow", "80x3+10+10", ")", "-reverse", "-background", "none", "-layers", "merge", "+repage", target_path]
    args = ["convert", source_path, "(", "-clone", "0", "-background", color_string, "-shadow", "80x3+10+10", ")", "-reverse", "-background", "none", "-layers", "merge", "+repage", target_path]
    subprocess.run(args, capture_output=True)


def main():
    # Setup
    # Set up command line options
    parser = argparse.ArgumentParser(description='Generate XKCD wallpapers.')
    parser.add_argument('-b', '--bgcolor', default="#EAD494", dest='bgcolor', action='store', help='color value in hex notation')
    parser.add_argument('-n', '--comicnum', default="random", dest='comicnum', action='store', help='which comic to use')
    args = parser.parse_args()

    setup_cache_dir()

    # Get a random comic URL
    url = get_random_comic()

    # Grab the image
    download_image(url, setup_cache_dir())

    add_drop_shadow(args.bgcolor)
    add_background(args.bgcolor)



main()

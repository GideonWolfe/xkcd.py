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

# checks and creats the cache directory
def setup_cache_dir():
    homedir = os.path.expanduser("~") # without the ending /
    cachedir = homedir+"/.cache/xkcd"
    if os.path.isdir(cachedir):
        #  print("Cache directory found... Continuing")
        return(cachedir)
    else:
        #  print("No cache directory found... Creating")
        os.mkdir(cachedir)
        return(cachedir)

# Cleans up artifacts of building the image
def cleanup_cache_dir():
    homedir = os.path.expanduser("~") # without the ending /
    cachedir = homedir+"/.cache/xkcd/"
    shadowfile = cachedir+"shadowcomic.png"
    originalcomic = cachedir+"comic.png"
    if os.path.isfile(shadowfile):
        os.remove(shadowfile)
    if os.path.isfile(originalcomic):
        os.remove(originalcomic)

# Takes an image URL and saves it to $HOME/.cache/xkcd/comic.ext
def download_image(url, cacheDir):
    full_path = cacheDir + "/comic.png"
    urllib.request.urlretrieve(url, full_path)


# takes the comic with shadow and sticks a background on it
def add_background(bgcolor, size):
    source_path = setup_cache_dir() + "/shadowcomic.png"
    target_path = setup_cache_dir() + "/background.png"
    cmdargs = ["convert", source_path, "-gravity", "center", "-background", bgcolor, "-extent", size, target_path]
    subprocess.run(cmdargs, capture_output=True)


# Calculates color of shadow
def generate_shadow_color(bgcolor):
    rawHex = bgcolor.lstrip("#")
    rgb = tuple(int(rawHex[i:i+2], 16) for i in (0, 2, 4))
    colorList = list(rgb)
    for i in range(0, len(colorList)):
        colorList[i] = int(colorList[i]*0.8)
    rgb = tuple(colorList)
    return(rgb)

# adds the drop shadow to the comic
def add_drop_shadow(bgcolor):
    shadow_color = list(generate_shadow_color(bgcolor))
    color_string = "rgb({},{},{})".format(shadow_color[0], shadow_color[1], shadow_color[2])
    source_path = setup_cache_dir() + "/comic.png"
    target_path = setup_cache_dir() + "/shadowcomic.png"
    args = ["convert", source_path, "(", "-clone", "0", "-background", color_string, "-shadow", "80x3+10+10", ")", "-reverse", "-background", "none", "-layers", "merge", "+repage", target_path]
    subprocess.run(args, capture_output=True)


def main():
    # Setup
    # Set up command line options
    parser = argparse.ArgumentParser(description='Generate XKCD wallpapers.')
    comic_source = parser.add_mutually_exclusive_group(required=True)
    comic_source.add_argument('-c', '--comicnum', default="1", dest='comicnum', action='store', help='which comic to use')
    comic_source.add_argument('-r', '--random', default="False", dest='randomcomic', action='store_true', help='use random comic') # need to make this a boolean flag
    parser.add_argument('-b', '--bgcolor', default="#EAD494", dest='bgcolor', action='store', help='color value in hex notation')
    parser.add_argument('-s', '--size', default="1920x1080", dest='size', action='store', help='resolution to create the wallpaper')
    args = parser.parse_args()

    setup_cache_dir()

    url = ""
    if args.randomcomic == True:
        # Get a random comic URL
        url = get_random_comic()
    else:
        # Get a specific comic URL
        url = get_comic(args.comicnum)


    # Grab the image
    download_image(url, setup_cache_dir())
    add_drop_shadow(args.bgcolor)
    add_background(args.bgcolor, args.size)

    cleanup_cache_dir()



main()

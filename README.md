# xkcd.py

A stupid simple script that grabs an XKCD comic, adds a little drop shadow and a background, and saves the result.

![](https://i.imgur.com/7TsDZcD.png)
![](https://i.imgur.com/YpFxi2V.png)
![](https://i.imgur.com/0XQVGND.png)

## Usage

```bash
usage: xkcd.py [-h] (-c COMICNUM | -r) [-b BGCOLOR] [-s SIZE]

Generate XKCD wallpapers.

options:
  -h, --help            show this help message and exit
  -c COMICNUM, --comicnum COMICNUM
                        which comic to use
  -r, --random          use random comic
  -b BGCOLOR, --bgcolor BGCOLOR
                        color value in hex notation
  -s SIZE, --size SIZE  resolution to create the wallpaper. default 1920x1080
```

## Dependencies

* ImageMagick
* python3

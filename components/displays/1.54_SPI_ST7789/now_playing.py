#!/usr/bin/env python3

# Get info from current playing song
# and send to the display

import requests

import ST7789

from time import sleep
from os.path import exists

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

HOMEPATH = "/home/pi/RPi-Jukebox-RFID"
DEFAULT_IMG = "/home/pi/RPi-Jukebox-RFID/shared/logo.png"

# Grab the path to the Audio Folders
with open(f"{HOMEPATH}/settings/Audio_Folders_Path", 'r') as audio:
    AFP = audio.read().replace("\n", "")

# Create the display object
disp = ST7789.ST7789(
    port=1,
    cs=ST7789.BG_SPI_CS_BACK,  # BG_SPI_CS_BACK or BG_SPI_CS_FRONT
    dc=26,
    backlight=19,               # 18 for back BG slot, 19 for front BG slot.
    spi_speed_hz=80 * 1000 * 1000,
)

# Initialize display.
disp.begin()

previous = ''

while True:
    # Check if anything is playing or has been played. On boot up, nothing has
    # been played, so file, artist, title, etc don't exist
    info = requests.get('http://192.168.86.33/api/player.php').json()

    if 'file' in info:

        if "title" in info:
            title = info['title']
        else:
            title = info['file']


        # To save on CPU and Memory, if the song hasn't changed, then skip all
        # the stuff
        if (previous == title):
            continue
        else:
            previous = title

        # Make the title multi-line if it is longer than 20 characters
        title = '\n'.join(title[n:n + 20] for n in range(0, len(title), 20))

        if "artist" in info:
            artist = info['artist']
            # Make the artist multi-line if it is longer than 20 characters
            artist = '\n\n' + '\n'.join(artist[n:n + 20] for n in range(0, len(artist), 20))
        else:
            artist = ''

        # Get the current album being played to get the cover art. Sleep for a
        # second so the file can get updated before grabbing contents.
        sleep(1)
        with open(f"{HOMEPATH}/settings/Latest_Folder_Played", 'r') as latest:
            LFP = latest.read().replace("\n", "")

        cover_art = AFP + "/" + LFP + "/cover.jpg"

        if exists(cover_art):
            img = Image.open(cover_art)
        else:
            img = Image.open(DEFAULT_IMG)

        img = img.resize((disp.width, disp.height)).convert("RGBA")
        txt = Image.new('RGBA', img.size, (255,255,255,0))
        draw = ImageDraw.Draw(txt)

        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)

        song_info = title + artist
        text_x, text_y = draw.textsize(song_info, font)
        draw.rectangle((0, 0, disp.width, text_y + 12), fill=(0,0,0,80))
        draw.text((4,4), song_info, font=font, fill=(255, 255, 255))

        combined = Image.alpha_composite(img, txt)
        disp.display(combined)

    else:
        img = Image.open(DEFAULT_IMG)
        img = img.resize((disp.width, disp.height))

        draw = ImageDraw.Draw(img)

        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)

        draw.text((4,4), "Select a song to play", font=font, fill=(255, 255, 255))
        disp.display(img)


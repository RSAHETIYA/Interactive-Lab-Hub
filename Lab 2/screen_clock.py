import time
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789
import datetime

# Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 64000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

# Create the ST7789 display:
disp = st7789.ST7789(
    spi,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
    width=135,
    height=240,
    x_offset=53,
    y_offset=40,
)

# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
height = disp.width  # we swap height/width to rotate it to landscape!
width = disp.height
image = Image.new("RGB", (width, height))
rotation = 90

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
disp.image(image, rotation)
# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

# Alternatively load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)

# Turn on the backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True

while True:
    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    #TODO: Lab 2 part D work should be filled in here. You should be able to look in cli_clock.py and stats.py 
    y = top
    draw.text((5, 5), "HI :D", font=font, fill=(255, 255, 255))

    draw.line([(210, height-11), (230, height-11)], fill=(255, 0, 0))
    draw.line([(210, height-11), (210, height-70)], fill=(255, 0, 0))
    draw.line([(230, height-11), (230, height-70)], fill=(255, 0, 0))

    draw.line([(130, height-11), (170, height-11)], fill=(255, 255, 0))
    draw.line([(130, height-11), (130, height-80)], fill=(255, 255, 0))
    draw.line([(170, height-11), (170, height-80)], fill=(255, 255, 0))

    draw.line([(10, height-11), (100, height-11)], fill=(0, 255, 0))
    draw.line([(10, height-11), (10, height-90)], fill=(0, 255, 0))
    draw.line([(100, height-11), (100, height-90)], fill=(0, 255, 0))

    now = datetime.datetime.now().time()
    hour = now.hour + 10
    binaryhour = bin(hour).replace("0b", "").zfill(5)

    if binaryhour[4] == "1":
        draw.line([(230, 10), (225, 10)], fill=(0, 0, 255)) 
    else:
        draw.line([(230, 10), (225, 10)], fill=(255, 0, 0)) 
    if binaryhour[3] == "1":
        draw.line([(215, 10), (210, 10)], fill=(0, 0, 255)) 
    else:
        draw.line([(215, 10), (210, 10)], fill=(255, 0, 0))
    if binaryhour[2] == "1":
        draw.line([(200, 10), (195, 10)], fill=(0, 0, 255))
    else:
         draw.line([(200, 10), (195, 10)], fill=(255, 0, 0))
    if binaryhour[1] == "1":
        draw.line([(185, 10), (180, 10)], fill=(0, 0, 255)) 
    else:
        draw.line([(185, 10), (180, 10)], fill=(255, 0, 0)) 
    if binaryhour[0] == "1":
        draw.line([(170, 10), (165, 10)], fill=(0, 0, 255)) 
    else:
        draw.line([(170, 10), (165, 10)], fill=(255, 0, 0)) 

    for i in range(hour * 3):
        draw.line([(11, height-12-i), (99, height-12-i)], fill=(0, 0, 255))

    for i in range(now.minute):
        draw.line([(131, height-12-i), (169, height-12-i)], fill=(0, 0, 255))
    
    for i in range(now.second):
        draw.line([(211, height-12-i), (229, height-12-i)], fill=(0, 0, 255))

    #print(now.time().hour + now.time().minute + now.time().second)

    # Display image.
    disp.image(image, rotation)
    time.sleep(1)

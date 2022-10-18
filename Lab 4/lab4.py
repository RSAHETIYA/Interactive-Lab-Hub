import time
import board
import busio
import musicalbeeps
import digitalio as digitalio2

import adafruit_mpr121
from adafruit_seesaw import seesaw, rotaryio, digitalio

from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789
from adafruit_rgb_display.rgb import color565

# Setup SPI bus using hardware SPI:
spi = board.SPI()

# Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
cs_pin = digitalio2.DigitalInOut(board.CE0)
dc_pin = digitalio2.DigitalInOut(board.D25)
reset_pin = None


# Config for display baudrate (default max is 24mhz):
BAUDRATE = 64000000

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

height = disp.width  # we swap height/width to rotate it to landscape!
width = disp.height
image = Image.new("RGB", (width, height))
rotation = 90

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)
disp.image(image, rotation)

# Turn on the backlight
backlight = digitalio2.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True

draw.rectangle((0, 0, width, height), outline=0, fill=(0, 255, 255))

i2c = busio.I2C(board.SCL, board.SDA)
seesaw = seesaw.Seesaw(board.I2C(), addr=0x36)
seesaw.pin_mode(24, seesaw.INPUT_PULLUP)
button = digitalio.DigitalIO(seesaw, 24)
button_held = False
encoder = rotaryio.IncrementalEncoder(seesaw)

mpr121 = adafruit_mpr121.MPR121(i2c)
player = musicalbeeps.Player(volume = 0.1,
                            mute_output = False)



while True:

    player.volume  = (-encoder.position % 100) / 100

    disp.fill(color565(0, int(255 * player.volume), 0))
    if mpr121[0].value:
        player.play_note("A", .25)
    elif mpr121[1].value:
        player.play_note("A#", .25)
    elif mpr121[2].value:
        player.play_note("B", .25)
    elif mpr121[3].value:
        player.play_note("C", .25)
    elif mpr121[4].value:
        player.play_note("C#", .25)
    elif mpr121[5].value:
        player.play_note("D", .25)
    elif mpr121[6].value:
        player.play_note("D#", .25)
    elif mpr121[7].value:
        player.play_note("E", .25)
    elif mpr121[8].value:
        player.play_note("F", .25)
    elif mpr121[9].value:
        player.play_note("F#", .25)
    elif mpr121[10].value:
        player.play_note("G", .25)
    elif mpr121[11].value:
        player.play_note("G#", .25)
    else:
        player.play_note("pause", .25)
    time.sleep(.25)  # Small delay to keep from spamming output messages.

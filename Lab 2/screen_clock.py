import time
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
from adafruit_seesaw import seesaw, rotaryio
from adafruit_seesaw import digitalio as rotaryIO
import adafruit_rgb_display.st7789 as st7789
import datetime
import qwiic_button 
import adafruit_mpr121


# Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 64000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

seesaw = seesaw.Seesaw(board.I2C(), addr=0x36)
encoder = rotaryio.IncrementalEncoder(seesaw)
green_button = qwiic_button.QwiicButton()
mpr121 = adafruit_mpr121.MPR121(board.I2C())
button_display_a = digitalio.DigitalInOut(board.D23)
button_display_b = digitalio.DigitalInOut(board.D24)

# 0 = clock
# 1 = timer
primary_mode = 0

# If timer is set or not
timer_set = False
current_timer = 0
hour_timer = 0
minute_timer = 0
second_timer = 0
start_time = None

# Timer mode being set
current_timer_denom = "hours"

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
rotary_button = rotaryIO.DigitalIO(seesaw, 24)
# Alternatively load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)

# Turn on the backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True
green_button.LED_off()
button_held = False

def draw_bins():
    draw.line([(210, height-11), (230, height-11)], fill=(255, 0, 0))
    draw.line([(210, height-11), (210, height-70)], fill=(255, 0, 0))
    draw.line([(230, height-11), (230, height-70)], fill=(255, 0, 0))

    draw.line([(130, height-11), (170, height-11)], fill=(255, 255, 0))
    draw.line([(130, height-11), (130, height-80)], fill=(255, 255, 0))
    draw.line([(170, height-11), (170, height-80)], fill=(255, 255, 0))

    draw.line([(10, height-11), (100, height-11)], fill=(0, 255, 0))
    draw.line([(10, height-11), (10, height-90)], fill=(0, 255, 0))
    draw.line([(100, height-11), (100, height-90)], fill=(0, 255, 0))

def clock_display():

    draw_bins()

    draw.text((5, 5), "Clock :D", font=font, fill=(255, 255, 255))

    now = datetime.datetime.now().time()
    hour = now.hour
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

def calculate_time_left():
    global start_time
    global hour_timer
    global minute_timer
    global second_timer

    now = datetime.datetime.now()
    time_elapsed = now - start_time
    time_elapsed = datetime.timedelta(seconds=current_timer) - time_elapsed
    seconds = time_elapsed.total_seconds()
    hour_timer_div = divmod(seconds, 3600)     
    hour_timer = int(hour_timer_div[0])   
    minute_timer_div = divmod(hour_timer_div[1], 60)  
    minute_timer = int(minute_timer_div[0])          
    second_timer_div = divmod(minute_timer_div[1], 1) 
    second_timer = int(second_timer_div[0])
    
    return time_elapsed

def draw_timer():

    global hour_timer
    global minute_timer
    global second_timer

    for i in range(hour_timer * 3):
                draw.line([(11, height-12-i), (99, height-12-i)], fill=(0, 0, 255))
    for i in range(minute_timer):
        draw.line([(131, height-12-i), (169, height-12-i)], fill=(0, 0, 255))
    
    for i in range(second_timer):
        draw.line([(211, height-12-i), (229, height-12-i)], fill=(0, 0, 255))

def timer_display():
    draw_bins()

    #draw.text((5, 5), "Timer :D", font=font, fill=(255, 255, 255))
    global timer_set
    global current_timer_denom
    global current_timer
    global button_held
    global hour_timer
    global minute_timer
    global second_timer
    global start_time
    global primary_mode

    if not rotary_button.value and not button_held:
        button_held = True

    draw_timer()

    if (timer_set):
        draw.text((5, 5), "Timer Started :D", font=font, fill=(255, 255, 255))
        if calculate_time_left().days < 0:
            primary_mode = 2
        
    else:
        draw.text((5, 5), "Timer :D", font=font, fill=(255, 255, 255))
        if (current_timer_denom == "hours"):
            hour_timer = abs(-encoder.position) % 24
            if rotary_button.value and button_held:
                button_held = False
                current_timer_denom = "minutes"
        elif (current_timer_denom == "minutes"):
            minute_timer = abs(-encoder.position) % 60
            if rotary_button.value and button_held:
                button_held = False
                current_timer_denom = "seconds"
        else:
            second_timer = abs(-encoder.position) % 60
            green_button.LED_on(100)
            if rotary_button.value and button_held:
                button_held = False
                current_timer_denom = "hours"
                green_button.LED_off()
            if (green_button.is_button_pressed()):
                current_timer = 3600 * hour_timer + 60 * minute_timer + second_timer
                green_button.LED_off()
                current_timer_denom = "hours"
                timer_set = True
                start_time = datetime.datetime.now()

while True:

    if (-encoder.position < 0):
        encoder.position = 0
    if (-encoder.position > 255):
        encoder.position = -255

    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    #TODO: Lab 2 part D work should be filled in here. You should be able to look in cli_clock.py and stats.py 
    
    if (primary_mode == 2):
        draw.rectangle((0, 0, width, height), outline=0, fill=(255, 0, 0))
        draw.text((120, 65), "BEEP!!!", font=font, fill=(255, 255, 255))
        if (mpr121[0].value):
            current_timer = 0
            timer_set = False
            current_timer_denom = "hours"
            primary_mode = 0

    if (not button_display_a.value and primary_mode == 1):
        green_button.LED_off()
        current_timer = 0
        timer_set = False
        current_timer_denom = "hours"
        primary_mode = 0

    if (not button_display_b.value and primary_mode == 0):
        primary_mode = 1

    if (primary_mode == 0):
        clock_display()
    elif (primary_mode == 1):
        timer_display()

    # Display image.
    disp.image(image, rotation)
    time.sleep(.1)

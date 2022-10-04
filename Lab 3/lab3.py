import board
import digitalio
import busio
import random
from adafruit_apds9960.apds9960 import APDS9960
import subprocess
from vosk import Model, KaldiRecognizer
import sys
import os
import wave
import time
import json
import qwiic_button
import requests
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789
from adafruit_rgb_display.rgb import color565

# Setup SPI bus using hardware SPI:
spi = board.SPI()

# Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None
i2c = board.I2C()

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
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True

apds = APDS9960(i2c)
apds.enable_proximity = True
green_button = qwiic_button.QwiicButton()

record = 'arecord -D hw:1,0 -f cd -c1 -r 16000 -d 5 -t wav recorded_mono.wav'
model = Model("model")

api_endpoint = "https://api.openweathermap.org/data/2.5/forecast"
api_key = "155bc49d500e165e0f9d2d54c30c173b"
weather_params = {
  "lat": 40.71,
  "lon": -74.01,
  "appid": api_key,
}

state = "Idle"
text = ""
wf = None

draw.rectangle((0, 0, width, height), outline=0, fill=(0, 255, 0))

while True:

    if state == "Idle":
        green_button.LED_off()
        disp.fill(color565(0, 0, 0))
        text = ""
        if (apds.proximity > 10):
            state = "Recording"
    elif state == "Recording":
        green_button.LED_on(100)
        record_p = subprocess.Popen(record, shell=True)
        disp.fill(color565(0, 255, 0))
        time.sleep(1)
        disp.fill(color565(55, 205, 0))
        time.sleep(1)
        disp.fill(color565(155, 155, 0))
        time.sleep(1)
        disp.fill(color565(205, 105, 0))
        time.sleep(1)
        disp.fill(color565(255, 55, 0))
        time.sleep(1)
        disp.fill(color565(0, 0, 255))
        wf = wave.open("recorded_mono.wav", "rb")
        rec = KaldiRecognizer(model, wf.getframerate(), '["weather", "water", "time", "[unk]"]')
        state = "Interpret"
    elif state == "Interpret":
        green_button.LED_off()
        data = wf.readframes(4000)
        if len(data) == 0:
            state = "Talking"
        else:
            if rec.AcceptWaveform(data):
                (rec.Result())
            else:
                (rec.PartialResult())

            txt = json.loads(rec.FinalResult()).get("text")
            if txt != "":
                text += txt
                state = "Talking"
    elif state == "Talking":
        disp.fill(color565(0, 0, 0))
        talk_text = ""
        if text == "water":
            if random.random() < .5:
                talk_text = "Yes, it is time to water the plant now"
            else:
                talk_text = "No, it is not time to water the plant"
        elif text == "weather":
            response = requests.get(api_endpoint, params=weather_params)
            response.raise_for_status()
            weather_data = response.json()
            i = 0
            for list in weather_data["list"]:
                print(list["pop"])
                if i == 4:
                    talk_text = "it will not rain within the next 12 hours"
                    break
                if list["pop"] > .8:
                    talk_text = "it will rain within the next 12 hours"
                    break
                i+=1
        elif text == "time":
            now = datetime.now()
            time = now.strftime("%H:%M")
            talk_text = "It is " + time
        else:
            talk_text = "Sorry, I cannot interpret what you just said, please try again"
        
        say = subprocess.Popen('say() { local IFS=+;/usr/bin/mplayer -ao alsa -really-quiet -noconsolecontrols "http://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&q=$*&tl=en"; } ; say "' +  talk_text + '"', shell=True)
        if say.poll() is None:
            if talk_text == "Yes, it is time to water the plant now":
                time.sleep(5)
                talk_text = "Ok, now stop watering"
                say = subprocess.Popen('say() { local IFS=+;/usr/bin/mplayer -ao alsa -really-quiet -noconsolecontrols "http://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&q=$*&tl=en"; } ; say "' +  talk_text + '"', shell=True)
                time.sleep(1)
            state = "Idle"
        
    time.sleep(.1)
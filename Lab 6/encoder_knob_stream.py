import time
import board
import busio
from adafruit_seesaw import seesaw, rotaryio, digitalio


import paho.mqtt.client as mqtt
import uuid

client = mqtt.Client(str(uuid.uuid1()))
client.tls_set()
client.username_pw_set('idd', 'device@theFarm')

client.connect(
    'farlab.infosci.cornell.edu',
    port=8883)

topic = 'IDD/your/topic/here'

seesaw = seesaw.Seesaw(board.I2C(), addr=0x36)
seesaw.pin_mode(24, seesaw.INPUT_PULLUP)
button = digitalio.DigitalIO(seesaw, 24)
button_held = False
encoder = rotaryio.IncrementalEncoder(seesaw)

last = encoder.position

while True:
    if encoder.position != last:
        val = "The encoder has been rotated to: " + str(encoder.position)
        client.publish(topic, val)
    last = encoder.position
    time.sleep(0.25)

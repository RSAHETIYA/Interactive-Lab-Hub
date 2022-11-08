import time
import paho.mqtt.client as mqtt
import uuid
import signal
import certifi


topic = 'IDD/rs2248/lab6'

def on_connect(client, userdata, flags, rc):
    print(f"connected with result code {rc}")
    client.subscribe(topic)

def on_message(cleint, userdata, msg):
    # if a message is recieved on the colors topic, parse it and set the color
    if msg.topic == topic and msg.payload.decode('UTF-8') == "bin is full":
        print("The bin has filled up")
    if msg.topic == topic and msg.payload.decode('UTF-8') == "Open bin":
        print("Bin 1 has opened up, current bin layout is:")
        print("O || O || O || O")
    if msg.topic == topic and msg.payload.decode('UTF-8') == "Close bin":
        print("Bin 1 has filled up, current bin layout is:")
        print("X || O || O || O")

client = mqtt.Client(str(uuid.uuid1()))
client.tls_set(certifi.where())
client.username_pw_set('idd', 'device@theFarm')
client.on_connect = on_connect
client.on_message = on_message

client.connect(
    'farlab.infosci.cornell.edu',
    port=8883)

client.loop_start()

# this lets us exit gracefully (close the connection to the broker)
def handler(signum, frame):
    print('exit gracefully')
    client.loop_stop()
    exit (0)

# our main loop
while True:
    nextmessage= input()
    client.publish(topic, nextmessage)
    
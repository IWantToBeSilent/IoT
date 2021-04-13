import paho.mqtt.client as mqtt
import json
from collections import deque
import matplotlib.pyplot as plt
import matplotlib.animation as animation
mess=1
client = mqtt.Client()

def off_disconnect():
    global client
    client.loop_stop()
    print('Disconnect')

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe("raspberry/co2")

def on_message(client, userdata, msg):
    global mess
    global date_Time
    parsed_msg = json.loads(msg.payload)
    co2_ppm = int(parsed_msg["CO2"])
    mess=co2_ppm
    #date = parsed_msg["Date"]
    #print(f'{co2_ppm} {date}\n')


def init():
    global client

    client.on_connect = on_connect

    client.will_set('raspberry/status', '{"status": "Off"}')

    client.connect("broker.hivemq.com", 1883, 60)

    client.on_message = on_message
    client.loop_start()

#while True:
    #init()
    #print(mess)
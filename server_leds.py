import paho.mqtt.client as mqtt
import time
import board
import busio
import adafruit_ccs811
import json
from gpiozero import LED

ledG = LED(21)
ledR = LED(20)

def on_connect(client, userdata, flags, rc):
        print(f"Connected with result code {rc}")
        client.subscribe("raspberry/leds")

def on_message(client, userdata, msg):
        global ledG
        global ledR
        parsed_msg = json.loads(msg.payload)
        ledG_on = parsed_msg["ledG"]
        ledR_on = parsed_msg["ledR"]
        if ledG_on == False and ledR_on == False:
                ledG.off()
                ledR.off()
        elif ledG_on == True and ledR_on == False:
                ledG.on()
                ledR.off()
        elif ledG_on == False and ledR_on == True:
                ledG.off()
                ledR.on()

client = mqtt.Client()
client.on_connect = on_connect

client.will_set('raspberry/status', '{"status": "Off"}')

client.connect("broker.hivemq.com", 1883, 60)

client.on_message = on_message

client.loop_forever()
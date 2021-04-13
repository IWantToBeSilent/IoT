import paho.mqtt.client as mqtt
import time
import board
import busio
import adafruit_ccs811
import json
from datetime import datetime
from gpiozero import Button

button = Button(6)
button_click = False
ledG = False
ledR = False

def switch_button(button_click):
        if button_click == False:
                button_click = True
        else:
                button_click = False
        return button_click

def on_connect(client, userdata, flags, rc):
        print(f"Connected with result code {rc}")

client = mqtt.Client()
client.on_connect = on_connect
client.connect("broker.hivemq.com", 1883, 60)

i2c = busio.I2C(board.SCL, board.SDA)
ccs811 = adafruit_ccs811.CCS811(i2c)

count = 0
while True:
        if button.is_pressed:
                button_click = switch_button(button_click)
        if button_click == True:
                eco2 = ccs811.eco2
                if eco2 >= 1000:
                        ledG = False
                        ledR = True
                else:
                        ledG = True
                        ledR = False
                co2_msg = {
                        'CO2': eco2,
                        'TVOC': ccs811.tvoc,
                        'Date': datetime.strftime(datetime.now(), "%H:%M:%S")
                }
                client.publish('raspberry/co2', payload = json.dumps(co2_msg), qos=0, retain=False)
                print(f"send {count} to raspberry/topic")
                count += 1
        else:
                ledG = False
                ledR = False

        leds_msg = {
                'ledG': ledG,
                'ledR': ledR
        }
        client.publish('raspberry/leds', payload = json.dumps(leds_msg), qos=0, retain=False)
        #print("{} {}".format(ledG, ledR))
        if button_click == False:
                time.sleep(0.15)
                continue
        time.sleep(0.5)

client.loop_forever()

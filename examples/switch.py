#  Copyright (c) 2024 - Andreas Philipp
#  This code is published under the MIT license

# (c) Andreas Philipp - 2021
#  andreas.philipp@anphi.de

# simple demo script for a MQTT controlled switch
# The device registers itself in homeassistant via the homeassistant
# MQTT discovery protocol and shows up as switch
# when the device is switched on or off the accordingly callbacks are called
# on() and off() in this example


import time

from paho.mqtt.client import Client, CallbackAPIVersion

from ha_mqtt.mqtt_device_base import MqttDeviceSettings
from ha_mqtt.mqtt_switch import MqttSwitch

# instantiate an paho mqtt client and connect to the mqtt server
client = Client(CallbackAPIVersion.VERSION1, "testscript")
client.connect("localhost", 1883)
client.loop_start()


# callbacks for the on and off actions
def on():
    print("I got switched on")
    # report back as switched on
    sw.set_on()


def off():
    print("I got switched off")
    # report back as switched off
    sw.set_off()


# instantiate an MQTTSwitch object
settings = MqttDeviceSettings("sw1", 'mqtt-sw-1', client)
sw = MqttSwitch(settings)

# assign both callbacks
sw.callback_on = on
sw.callback_off = off

try:
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    pass
finally:
    # close the device for cleanup. Gets marked as offline/unavailable in homeassistant
    sw.close()
    client.loop_stop()
    client.disconnect()

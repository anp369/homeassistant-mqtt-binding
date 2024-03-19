#  Copyright (c) 2024 - Andreas Philipp
#  This code is published under the MIT license

# (c) Andreas Philipp - 2021
#  andreas.philipp@anphi.de

# simple demo script for a MQTT controlled switch and a set will.
# The device registers itself in homeassistant via the homeassistant
# MQTT discovery protocol and shows up as switch
# when the device is switched on or off the accordingly callbacks are called
# on() and off() in this example
#
# When losing connection, the will payload will be automatically published
# by the broker, showing the device as unavailable in HA


import time

from paho.mqtt.client import Client, CallbackAPIVersion

from ha_mqtt.mqtt_device_base import MqttDeviceSettings
from ha_mqtt.mqtt_switch import MqttSwitch
from ha_mqtt.util import HaSwitchDeviceClass

# instantiate a paho mqtt client and connect to the mqtt server
will_topic = "connections/conn-01/available"
client = Client(CallbackAPIVersion.VERSION2, "testscript")
client.will_set(will_topic, "offline", retain=True)


def init(*args, **kwargs):
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
    settings = MqttDeviceSettings("sw1", 'mqtt-sw-1', client, will_topic=will_topic)
    sw = MqttSwitch(settings, HaSwitchDeviceClass.SWITCH)

    # assign both callbacks
    sw.callback_on = on
    sw.callback_off = off


client.on_connect = init

client.connect("localhost", 1883)
client.loop_start()

try:
    print("started")
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    pass
finally:
    # close the device for cleanup. Gets marked as offline/unavailable in homeassistant
    client.disconnect()
    client.loop_stop()

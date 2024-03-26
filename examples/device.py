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

from ha_mqtt.ha_device import HaDevice
from ha_mqtt.mqtt_device_base import MqttDeviceSettings
from ha_mqtt.mqtt_switch import MqttSwitch

will_topic = "connections/conn-02/available"

# instantiate a paho mqtt client and connect to the mqtt server
client = Client(CallbackAPIVersion.VERSION2, "testscript")
client.will_set(will_topic, 'offline', retain=True)
client.connect("localhost", 1883)
client.loop_start()


# callbacks for the on and off actions
def on(entity: MqttSwitch, id: int):
    print(f"{id} got switched on")
    # report back as switched on
    entity.set_on()


def off(entity: MqttSwitch, id: int):
    print(f"{id} got switched off")
    # report back as switched off
    entity.set_off()


# create device info dictionary
dev = HaDevice("Testdevice", "test123456-veryunique")

# instantiate an MQTTSwitch object
sw1 = MqttSwitch(MqttDeviceSettings("sw-1", "idofsw1", client, dev, will_topic=will_topic))
sw2 = MqttSwitch(MqttDeviceSettings("sw-2", "idofsw2", client, dev, will_topic=will_topic))
sw3 = MqttSwitch(MqttDeviceSettings("sw-3", "idofsw3", client, dev, will_topic=will_topic))

# assign both callbacks
sw1.callback_on = lambda: on(sw1, 1)
sw1.callback_off = lambda: off(sw1, 1)

sw2.callback_on = lambda: on(sw2, 2)
sw2.callback_off = lambda: off(sw2, 2)

sw3.callback_on = lambda: on(sw3, 3)
sw3.callback_off = lambda: off(sw3, 3)

try:
    # start all devices, runs discovery
    sw1.start()
    sw2.start()
    sw3.start()
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    pass
finally:
    # close the device for cleanup. Gets marked as offline/unavailable in homeassistant
    sw1.stop()
    sw2.stop()
    sw3.stop()
    client.loop_stop()
    client.disconnect()

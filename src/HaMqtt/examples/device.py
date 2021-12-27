# (c) Andreas Philipp - 2021
#  andreas.philipp@anphi.de

# simple demo script for a MQTT controlled switch
# The device registers itself in homeassistant via the homeassistant
# MQTT discovery protocol and shows up as switch
# when the device is switched on or off the accordingly callbacks are called
# on() and off() in this example


import time

from paho.mqtt.client import Client

from src.HaMqtt.MQTTSwitch import MQTTSwitch

# instantiate an paho mqtt client and connect to the mqtt server
client = Client("testscript")
client.connect("localhost", 1883)
client.loop_start()


# callbacks for the on and off actions
def on(entity: MQTTSwitch, id: int):
    print(f"{id} got switched on")
    # report back as switched on
    entity.set_on()


def off(entity: MQTTSwitch, id: int):
    print(f"{id} got switched off")
    # report back as switched off
    entity.set_off()


# create device info dictionary
dev = {
    "identifiers": ["testschalter-00001"],
    "name": "Testschalter 1",
    "manufacturer": "Andreas Philipp"

}

# instantiate an MQTTSwitch object
sw1 = MQTTSwitch("sw1", "sw1", client, "testschalter-sw-01", dev)
sw2 = MQTTSwitch("sw2", "sw2", client, "testschalter-sw-02", dev)
sw3 = MQTTSwitch("sw3", "sw3", client, "testschalter-sw-03", dev)

# assign both callbacks
sw1.callback_on = lambda: on(sw1, 1)
sw1.callback_off = lambda: off(sw1, 1)

sw2.callback_on = lambda: on(sw2, 2)
sw2.callback_off = lambda: off(sw2, 2)

sw3.callback_on = lambda: on(sw3, 3)
sw3.callback_off = lambda: off(sw3, 3)

try:
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    pass
finally:
    # close the device for cleanup. Gets marked as offline/unavailable in homeassistant
    sw1.close()
    sw2.close()
    sw3.close()
    client.loop_stop()
    client.disconnect()

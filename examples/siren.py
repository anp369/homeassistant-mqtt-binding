#  Copyright (c) 2024 - Andreas Philipp
#  This code is published under the MIT license

import time

from paho.mqtt.client import Client, CallbackAPIVersion

from ha_mqtt.mqtt_device_base import MqttDeviceSettings
from ha_mqtt.mqtt_siren import MqttSiren

# instantiate an paho mqtt client and connect to the mqtt server
client = Client(CallbackAPIVersion.VERSION2, "testscript")
client.connect("localhost", 1883)
client.loop_start()


def alarming():
    siren.set_on()
    print("ALARMING!!!")
    time.sleep(5)
    print("Alarm done")
    siren.set_off()


settings = MqttDeviceSettings("Testsiren", "siren-01", client)
siren = MqttSiren(settings)

siren.callback_on = alarming

try:
    siren.start()
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    pass
finally:
    # close the device for cleanup. Gets marked as offline/unavailable in homeassistant
    siren.stop()
    client.loop_stop()
    client.disconnect()

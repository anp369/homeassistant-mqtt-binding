import time
import uuid

from paho.mqtt.client import Client

from src.HaMqtt.MQTTSiren import MQTTSiren

# instantiate an paho mqtt client and connect to the mqtt server
client = Client("testscript")
client.connect("localhost", 1883)
client.loop_start()


def alarming():
    siren.set_on()
    print("ALARMING!!!")
    time.sleep(5)
    print("Alarm done")
    siren.set_off()


siren = MQTTSiren("Testsirene", "siren-01", client, f"siren-{uuid.uuid4()}")

siren.callback_on = alarming

try:
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    pass
finally:
    # close the device for cleanup. Gets marked as offline/unavailable in homeassistant
    siren.close()
    client.loop_stop()
    client.disconnect()

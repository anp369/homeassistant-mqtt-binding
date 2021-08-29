# (c) Andreas Philipp - 2021
#  andreas.philipp@anphi.de


import time
from random import uniform

from paho.mqtt.client import Client

from src.HaMqtt.MQTTThermometer import MQTTThermometer

# instantiate an paho mqtt client and connect to the mqtt server
client = Client("testscript")
client.connect("localhost", 1883)
client.loop_start()

# callbacks for the on and off actions


# instantiate an MQTTThermometer object
th = MQTTThermometer("Thermometer 1", "temp1", client, "°C")

try:
    while True:
        # publish a random "temperature" every 5 seconds
        temp = f"{uniform(-10, 10):2.2f}"
        print(f"publishing temperature: {temp} {th.unit_of_measurement}")
        th.publish_state(temp)
        time.sleep(5)

except KeyboardInterrupt:
    pass
finally:
    # close the device for cleanup. Gets marked as offline/unavailable in homeassistant
    th.close()
    client.loop_stop()
    client.disconnect()

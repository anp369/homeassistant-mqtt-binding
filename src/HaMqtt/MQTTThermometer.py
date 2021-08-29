from paho.mqtt.client import Client

from .MQTTSensor import MQTTSensor
from .MQTTUtil import HaDeviceClass


class MQTTThermometer(MQTTSensor):
    def __init__(self, name: str, node_id: str, client: Client, unit: str = "°C"):
        super().__init__(name, node_id, client, unit, HaDeviceClass.TEMPERATURE)

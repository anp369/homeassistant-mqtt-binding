import uuid

from paho.mqtt.client import Client

from .MQTTSensor import MQTTSensor
from .MQTTUtil import HaDeviceClass


class MQTTThermometer(MQTTSensor):
    def __init__(self, name: str, node_id: str, client: Client, unit: str = "°C", unique_id=str(uuid.uuid4()),
                 device_dict: dict = None):
        super().__init__(name, node_id, client, unit, HaDeviceClass.TEMPERATURE, unique_id=unique_id,
                         device_dict=device_dict)

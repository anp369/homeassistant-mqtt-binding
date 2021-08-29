import uuid

from paho.mqtt.client import Client

from .MQTTDevice import MQTTDevice
from .MQTTUtil import HaDeviceClass


class MQTTSensor(MQTTDevice):
    device_type = "sensor"

    def __init__(self, name: str, node_id: str, client: Client, unit: str, device_class: HaDeviceClass,
                 unique_id=str(uuid.uuid4())):
        """
        create sensor instance
        :param name: as in MQTTDevice
        :param node_id: as in MQTTDevice
        :param client: as in MQTTDevice
        :param unit: string containing the unit of measurement, example: '°C'
        :param device_class: a entry of the deviceclass enum containing the device class as in
        https://www.home-assistant.io/integrations/sensor/#device-class
        :param unique_id: as in MQTTDevice
        """
        self.device_class = device_class
        self.unit_of_measurement = unit
        super().__init__(name, node_id, client, True, unique_id)

    def initialize(self):
        self.add_config_option("device_class", self.device_class.value)
        self.add_config_option("unit_of_measurement", self.unit_of_measurement)

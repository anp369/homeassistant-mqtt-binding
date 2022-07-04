"""
Andreas Philipp - 2022
<dev@anphi.de>
"""

#  Copyright (c) 2022 - Andreas Philipp
#  This code is published under the MIT license

from .mqtt_device_base import MqttDeviceBase, MqttDeviceSettings
from .util import HaDeviceClass


class MqttSensor(MqttDeviceBase):
    """
    class that implements an arbitrary sensor such as a thermometer


    :param unit: string containing the unit of measurement, example: '°C'
    :param device_class: a entry of the deviceclass enum containing the device class as in
           https://www.home-assistant.io/integrations/sensor/#device-class
    :param settings: as in :class:`~ha_mqtt.mqtt_device_base.MqttDeviceBase`

    .. hint::
       Use :meth:`~ha_mqtt.mqtt_device_base.MqttDeviceBase.publish_state`
       to send the actual sensor data to homeassistant

    """

    device_type = "sensor"

    def __init__(self, settings: MqttDeviceSettings, unit: str, device_class: HaDeviceClass
                 , send_only=False):
        """
        create sensor instance
        """
        self.device_class = device_class
        self.unit_of_measurement = unit
        super().__init__(settings, send_only)

    def pre_discovery(self):
        self.add_config_option("device_class", self.device_class.value)
        self.add_config_option("unit_of_measurement", self.unit_of_measurement)

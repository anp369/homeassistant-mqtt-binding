"""
Andreas Philipp - 2022
<dev@anphi.de>
"""

#  Copyright (c) 2024 - Andreas Philipp
#  This code is published under the MIT license

from .mqtt_device_base import MqttDeviceBase, MqttDeviceSettings
from .util import HaSensorDeviceClass


class MqttSensor(MqttDeviceBase):
    """
    class that implements an arbitrary sensor such as a thermometer

    :param unit_of_measurement: string containing the unit of measurement, example: '°C'
    :param device_class: :class:`~ha_mqtt.util.HaSensorDeviceClass` device class of this sensor
    :param settings: as in :class:`~ha_mqtt.mqtt_device_base.MqttDeviceBase`
    :param unit_of_measurement: unit of measurement of this sensor

    .. hint::
       Use :meth:`~ha_mqtt.mqtt_device_base.MqttDeviceBase.update_state`
       to send the actual sensor data to homeassistant

    """

    device_type = "sensor"

    def __init__(
            self,
            settings: MqttDeviceSettings,
            device_class: HaSensorDeviceClass,
            unit_of_measurement: str,
            send_only: bool = False,
    ):
        self.device_class = device_class
        self.unit_of_measurement = unit_of_measurement
        super().__init__(settings, send_only)

    def pre_discovery(self) -> None:
        self.add_config_option("device_class", self.device_class.value)
        self.add_config_option("unit_of_measurement", self.unit_of_measurement)

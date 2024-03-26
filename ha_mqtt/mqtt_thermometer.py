"""
this module contains all classes for implementing mqtt thermometers
"""

#  Copyright (c) 2024 - Andreas Philipp
#  This code is published under the MIT license

from .mqtt_sensor import MqttDeviceSettings, MqttSensor
from .util import HaSensorDeviceClass


class MqttThermometer(MqttSensor):
    """
    subclass of MqttSensor, measures temperatures.
    The default unit is °C and can be changed in the constructor
    """

    def __init__(
        self, settings: MqttDeviceSettings, unit: str = "°C", send_only: bool = True
    ):
        super().__init__(settings, HaSensorDeviceClass.TEMPERATURE, unit, send_only)

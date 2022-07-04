"""
this module contains all classes for implementing mqtt thermometers
"""

#  Copyright (c) 2022 - Andreas Philipp
#  This code is published under the MIT license

from .mqtt_sensor import MqttSensor, MqttDeviceSettings
from .util import HaDeviceClass


class MqttThermometer(MqttSensor):
    """
    subclass of MqttSensor, measures temperatures.
    The default unit is °C and can be changed in the constructor
    """

    def __init__(self, settings: MqttDeviceSettings, unit: str = "°C", send_only=True):
        super().__init__(settings, unit, HaDeviceClass.TEMPERATURE, send_only)

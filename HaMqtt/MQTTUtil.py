# helper file containing definitions

from enum import Enum

ON = b'on'
OFF = b'off'


class HaDeviceClass(Enum):
    NONE = 'None'
    BATTERY = 'battery'
    CURRENT = 'current'
    ENERGY = 'energy'
    HUMIDITY = 'humidity'
    ILLUMINANCE = 'illuminance'
    MONETARY = 'monetary'
    SIGNAL_STRENGTH = 'signal_strength'
    TEMPERATURE = 'temperature'
    POWER = 'power'
    POWER_FACTOR = 'power_factor'
    PRESSURE = 'pressure'
    TIMESTAMP = 'timestamp'
    VOLTAGE = 'voltage'
    CARBON_MONOXIDE = 'carbon_monoxide'
    CARBON_DIOXIDE = 'carbon_dioxide'

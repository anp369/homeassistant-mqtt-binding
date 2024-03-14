"""
Andreas Philipp - 2022
<dev@anphi.de>

helper module containing shared definitions and enums
"""

#  Copyright (c) 2024 - Andreas Philipp
#  This code is published under the MIT license

from enum import Enum

ON = b'on'
OFF = b'off'


class EntityCategory(Enum):
    """
    Enum representing the different entity classes introduced in 2021.11.
    Choose CONFIG for entities that configure a device and
    DIAGNOSTIC for entities that reveal additional read-only information about a device
    """
    PRIMARY = ""
    CONFIG = "config"
    DIAGNOSTIC = "diagnostic"


class HaSensorDeviceClass(Enum):
    """
    Enum representing the different sensor classes homeassistant provides
    See the following link for more info:
    https://www.home-assistant.io/integrations/sensor/
    """
    NONE = None
    APPARENT_POWER = "apparent_power"
    AIR_QUALITY = "aqi"
    ATMOS_PRESSURE = "atmospheric_pressure"
    BATTERY = 'battery'
    CARBON_DIOXIDE = "carbon_dioxide"
    CARBON_MONOXIDE = 'carbon_monoxide'
    CURRENT = 'current'
    DATA_RATE = "data_rate"
    DATA_SIZE = "data_size"
    DATE = "date"
    DISTANCE = "distance"
    DURATION = "duration"
    ENERGY = 'energy'
    ENERGY_STORAGE = 'energy_storage'
    ENUM = 'enum'
    FREQUENCY = "frequency"
    GAS = "gas"
    HUMIDITY = 'humidity'
    ILLUMINANCE = 'illuminance'
    IRRADIANCE = 'irradiance'
    MONETARY = 'monetary'
    MOISTURE = 'moisture'
    NITROGEN_DIOXIDE = "nitrogen_dioxide"
    NITROGEN_MONOXIDE = "nitrogen_monoxide"
    NITROUS_OXIDE = "nitrous_oxide"
    OZON = "ozone"
    PH = "ph"
    PM1 = "pm1"
    PM10 = "pm10"
    PM25 = "pm25"
    POWER_FACTOR = "power_factor"
    POWER = "power"
    PRECIPITATION = 'precipitation'
    PRECIPITATION_INTENSITY = 'precipitation_intensity'
    PRESSURE = "pressure"
    REACTIVE_POWER = "reactive_power"
    SIGNAL_STRENGTH = 'signal_strength'
    SOUND_PRESSURE = 'sound_pressure'
    SPEED = 'speed'
    SULPHUR_DIOXIDE = "sulphur_dioxide"
    TEMPERATURE = 'temperature'
    TIMESTAMP = 'timestamp'
    VOLATILE_ORGANIC_COMPOUNDS = "volatile_organic_compounds"
    VOLATILE_ORGANIC_COMPOUNDS_PARTS = 'volatile_organic_compounds_parts'
    VOLTAGE = 'voltage'
    VOLUME = 'volume'
    VOLUME_FLOW_RATE = 'volume_flow_rate'
    VOLUME_STORAGE = 'volume_storage'
    WATER = 'water'
    WEIGHT = 'weight'
    WIND_SPEED = 'wind_speed'


class HaBinarySensorDeviceClass(Enum):
    """
    Enum representing the different binary sensor classes homeassistant provides
    See the following link for more info:
    https://www.home-assistant.io/integrations/binary_sensor/
    """
    NONE = None
    BATTERY = 'battery'
    BATTERY_CHARGING = "battery_charging"
    CARBON_MONOXIDE = 'carbon_monoxide'
    COLD = "cold"
    CONNECTIVITY = "connectivity"
    DOOR = "door"
    GARAGE_DOOR = "garage_door"
    GAS = 'gas'
    HEAT = "heat"
    LIGHT = "light"
    LOCK = "lock"
    MOISTURE = "moisture"
    MOTION = "motion"
    MOVING = "moving"
    OCCUPANCY = "occupancy"
    OPENING = "opening"
    PLUG = "plug"
    POWER = "power"
    PRESENCE = "presence"
    PROBLEM = "problem"
    RUNNING = "running"
    SAFETY = "safety"
    SMOKE = "smoke"
    SOUND = "sound"
    TAMPER = "tamper"
    UPDATE = "update"
    VIBRATION = "vibration"
    WINDOW = "window"


class HaCoverDeviceClass(Enum):
    """
    Enum representing the different cover classes homeassistant provides
    See the following link for more info:
    https://www.home-assistant.io/integrations/cover/
    """
    NONE = None
    AWNING = "awning"
    BLIND = "blind"
    CURTAIN = "curtain"
    DAMPER = "damper"
    DOOR = 'door'
    GARAGE = "garage"
    GATE = "gate"
    SHADE = "shade"
    SHUTTER = "shutter"
    WINDOW = 'window'


class HaSwitchDeviceClass(Enum):
    """
    Enum representing the different switch classes homeassistant provides
    See the following link for more info:
    https://www.home-assistant.io/integrations/switch/
    """
    NONE = None
    OUTLET = "outlet"
    SWITCH = "switch"


class HaButtonDeviceClass(Enum):
    """
    Enum representing the different button classes homeassistant provides
    See the following link for more info:
    https://www.home-assistant.io/integrations/button/
    """
    NONE = None
    IDENTIFY = 'identify'
    RESTART = 'restart'
    UPDATE = 'update'


class HaHumidifierDeviceClass(Enum):
    """
    Enum representing the different humidifier classes homeassistant provides
    See the following link for more info:
    https://www.home-assistant.io/integrations/humidifier/
    """
    NONE = None
    DEHUMIDIFIER = 'dehumidifier'
    HUMIDIFIER = 'humidifier'


class HaNumberDeviceClass(Enum):
    """
    Enum representing the different number classes homeassistant provides
    See the following link for more info:
    https://www.home-assistant.io/integrations/number/
    """
    NONE = None
    APPARENT_POWER = "apparent_power"
    AIR_QUALITY = "aqi"
    ATMOS_PRESSURE = "atmospheric_pressure"
    BATTERY = 'battery'
    CARBON_DIOXIDE = "carbon_dioxide"
    CARBON_MONOXIDE = 'carbon_monoxide'
    CURRENT = 'current'
    DATA_RATE = "data_rate"
    DISTANCE = "distance"
    ENERGY = 'energy'
    ENERGY_STORAGE = 'energy_storage'
    FREQUENCY = "frequency"
    GAS = "gas"
    HUMIDITY = 'humidity'
    ILLUMINANCE = 'illuminance'
    IRRADIANCE = 'irradiance'
    MOISTURE = 'moisture'
    NITROGEN_DIOXIDE = "nitrogen_dioxide"
    NITROGEN_MONOXIDE = "nitrogen_monoxide"
    NITROUS_OXIDE = "nitrous_oxide"
    OZON = "ozone"
    PH = "ph"
    PM1 = "pm1"
    PM10 = "pm10"
    PM25 = "pm25"
    POWER_FACTOR = "power_factor"
    POWER = "power"
    PRECIPITATION = 'precipitation'
    PRECIPITATION_INTENSITY = 'precipitation_intensity'
    PRESSURE = "pressure"
    REACTIVE_POWER = "reactive_power"
    SIGNAL_STRENGTH = 'signal_strength'
    SOUND_PRESSURE = 'sound_pressure'
    SPEED = 'speed'
    SULPHUR_DIOXIDE = "sulphur_dioxide"
    TEMPERATURE = 'temperature'
    VOLATILE_ORGANIC_COMPOUNDS = "volatile_organic_compounds"
    VOLTAGE = 'voltage'
    VOLUME = 'volume'
    VOLUME_FLOW_RATE = 'volume_flow_rate'
    VOLUME_STORAGE = 'volume_storage'
    WATER = 'water'
    WEIGHT = 'weight'
    WIND_SPEED = 'wind_speed'

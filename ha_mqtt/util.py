"""
Andreas Philipp - 2022
<dev@anphi.de>

helper module containing shared definitions and enums
"""

#  Copyright (c) 2023 - Andreas Philipp
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


class HaDeviceClass(Enum):
    """
    Enum representing the different sensor classes homeassistant provides
    See the following links for more info:
    - https://www.home-assistant.io/integrations/cover/
    - for sensors: https://www.home-assistant.io/integrations/sensor/
    - for binary sensors: https://www.home-assistant.io/integrations/binary_sensor/
    """
    # sensors
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
    ENUM = 'enum'
    FREQUENCY = "frequency"
    GAS = "gas"
    HUMIDITY = 'humidity'
    ILLUMINANCE = 'illuminance'
    IRRADIANCE = 'irradiance'
    MONETARY = 'monetary'
    NITROGEN_DIOXIDE = "nitrogen_dioxide"
    NITROGEN_MONOXIDE = "nitrogen_monoxide"
    NITROUS_OXIDE = "nitrous_oxide"
    OZON = "ozone"
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
    VOLTAGE = 'voltage'
    VOLUME = 'volume'
    WATER = 'water'
    WEIGHT = 'weight'
    WIND_SPEED = 'wind_speed'

    # binary sensors
    BATTERY_CHARGING = "battery_charging"
    COLD = "cold"
    CONNECTIVITY = "connectivity"
    DOOR = "door"
    GARAGE_DOOR = "garage_door"
    HEAT = "heat"
    LIGHT = "light"
    LOCK = "lock"
    MOISTURE = "moisture"
    MOTION = "motion"
    MOVING = "moving"
    OCCUPANCY = "occupancy"
    OPENING = "opening"
    PLUG = "plug"
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

    # covers
    AWNING = "awning"
    BLIND = "blind"
    CURTAIN = "curtain"
    DAMPER = "damper"
    GARAGE = "garage"
    GATE = "gate"
    SHADE = "shade"
    SHUTTER = "shutter"

    # switches
    OUTLET = "outlet"
    SWITCH = "switch"

    # buttons
    RESTART = 'restart'

    # humidifier
    DEHUMIDIFIER = 'dehumidifier'
    HUMIDIFIER = 'humidifier'

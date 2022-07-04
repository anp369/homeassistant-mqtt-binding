"""
Andreas Philipp - 2022
<dev@anphi.de>

this module contains the HaDevice class
"""

#  Copyright (c) 2022 - Andreas Philipp
#  This code is published under the MIT license

import json


class HaDevice:
    """
    Class for configuring a device that groups multiple entities in homeassistant
    """

    def __init__(self, name: str, unique_id: str):
        """
        constructor
        :param name: friendly name of the device
        :param unique_id: one unique identifier that is used by HA to assign entities to this device
        """
        self._name = name
        self.config = {
            "name": name,
            "identifiers": [unique_id]
        }

    def __str__(self):
        return f"{self._name}: {self.get_json()}"

    def add_config_option(self, key: str, value, override: bool = False):
        """
        adds an arbitrary item to the device config.
        It must be json serializable (preferred lists, dicts and key/value pairs)
        :param key key to assign the setting to
        :param value settings item to be written to the config
        :param override if set to true, override an existing item if present
        """
        if self.config.get(key) and not override:
            raise ValueError(
                "You are trying to override an existing config option. Specify 'override = True' if this was intended")
        self.config[key] = value

    @property
    def identifiers(self) -> list:
        """
        gets all set identifiers of this device
        :return: list containing the identifiers
        """
        return self.config.get("identifiers", [])

    def append_identifier(self, identifier: str):
        """
        appends a new identifier to the identifier list
        Make sur eto only use unique identifiers
        :param identifier: the identifier to add
        :raises ValueError: if the identifier already exists in the list
        """
        if identifier in self.config["identifiers"]:
            raise ValueError("identifier is already present")
        self.config["identifiers"].append(identifier)

    def get_json(self) -> str:
        """
        returns the json representation of the current configuration
        :return: json representation of the config
        """
        return json.dumps(self.config)

    def get_dict(self) -> dict:
        """
        returns the current configuration dict
        :return: dict containing the config
        """
        return self.config

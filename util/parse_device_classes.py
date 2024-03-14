#  Copyright (c) 2024 - Andreas Philipp
#  This code is published under the MIT license

"""
this file takes all device classes for
sensors, binary sensors, buttons, covers, numbers, switches and humidifiers
and compares them against the values in ha_mqtt.util and prints out values not in it
"""
import sys
from enum import Enum
from typing import Tuple, Set

import requests

from ha_mqtt.util import (HaBinarySensorDeviceClass, HaSwitchDeviceClass,
                          HaHumidifierDeviceClass, HaCoverDeviceClass,
                          HaSensorDeviceClass, HaButtonDeviceClass, HaNumberDeviceClass)

configuration = {
    HaSensorDeviceClass: {
        'url': "https://raw.githubusercontent.com/home-assistant/core/dev/homeassistant/components/sensor/strings.json"},
    HaBinarySensorDeviceClass: {
        'url': "https://raw.githubusercontent.com/home-assistant/core/dev/homeassistant/components/binary_sensor/strings.json"},
    HaButtonDeviceClass: {
        'url': "https://raw.githubusercontent.com/home-assistant/core/dev/homeassistant/components/button/strings.json"},
    HaCoverDeviceClass: {
        'url': "https://raw.githubusercontent.com/home-assistant/core/dev/homeassistant/components/cover/strings.json"},
    HaSwitchDeviceClass: {
        'url': "https://raw.githubusercontent.com/home-assistant/core/dev/homeassistant/components/switch/strings.json"},
    HaNumberDeviceClass: {
        'url': "https://raw.githubusercontent.com/home-assistant/core/dev/homeassistant/components/number/strings.json"},
    HaHumidifierDeviceClass: {
        'url': "https://raw.githubusercontent.com/home-assistant/core/dev/homeassistant/components/humidifier/strings.json"}
}


def fetch_items_by_url(url: str) -> Set[str]:
    try:
        response = requests.get(url)
        dictionary = response.json()

    except Exception as ex:
        print(f"Error fetching info for {url}:\n {ex}")
        sys.exit(1)

    target_set = set()

    for k in dictionary.get('entity_component').keys():
        if k == '_':
            target_set.add(None)
        else:
            target_set.add(k)
    return target_set


def compare_items(target: Set[str], actual: Enum) -> Tuple[bool, Set[str], Set[str]]:
    """
    compares both sets and determines missing new items present in the web documentation of HA (target).
    Also determines items present in the current code (actual) but not on the website anymore.
    These get classified as deprecated
    :param target: set from the HA documentation website
    :param actual: set from the code
    :return: bool - True if the code set is equal to the documentation set;
        Set - contains missing items in the code;
        Set - contains deprecated items in the code;
    """
    actual = {el.value for el in actual}
    missing = target - actual  # target \ actual
    deprecated = actual - target  # actual \ target

    return len(missing) == 0 and len(deprecated) == 0, missing, deprecated


def main():
    code_ok = True  # flag whether all items are in sync with the web docs
    for enum, config in configuration.items():
        if url := config.get('url'):
            target = fetch_items_by_url(url)
        if items := config.get('items'):
            target = set(items)

        in_sync, missing, deprecated = compare_items(target, enum)
        code_ok &= in_sync

        print(50 * '=')
        print(f"{enum}\n")
        if l := len(missing):
            print(f"found {l} missing entries:")
            for item in missing:
                if item == None:
                    print(f"NONE = '{item}'")
                else:
                    print(f"{item.upper()} = '{item}'")

        if l := len(deprecated):
            print(f"\nfound {l} deprecated entries:")
            for item in deprecated:
                print(f"{item}")

        if len(deprecated) == 0 and len(missing) == 0:
            print("OK!")

        print("")

    if not code_ok:
        sys.exit(1)


if __name__ == '__main__':
    main()

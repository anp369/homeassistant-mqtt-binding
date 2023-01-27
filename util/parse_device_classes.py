#  Copyright (c) 2023 - Andreas Philipp
#  This code is published under the MIT license

"""
this file takes all device classes for
sensors: https://www.home-assistant.io/integrations/sensor/

and compares them against the values in ha_mqtt.util and prints out values not in it
"""
import sys

import requests
from bs4 import BeautifulSoup

from ha_mqtt.util import HaDeviceClass

urls = {
    'binary_sensor': "https://www.home-assistant.io/integrations/binary_sensor/",
    'sensor': "https://www.home-assistant.io/integrations/sensor/",
    'button': "https://www.home-assistant.io/integrations/button",
    'cover': "https://www.home-assistant.io/integrations/cover/",
    'number': "https://www.home-assistant.io/integrations/number",
    'switch': "https://www.home-assistant.io/integrations/number",
}


def parse_url(url: str) -> set:
    """
    fetches the sensor device classes and compares it against the present types
    :param url: URL to fetch
    :return:
    """
    try:
        page = requests.get(url).content
        bs = BeautifulSoup(page, 'html.parser')
    except requests.exceptions.ConnectionError as ex:
        print(f"Can't fetch {url} : {ex}")
        sys.exit(1)

    list_elements = bs.find('article').find('ul').find_all('strong')
    known_el = {el.value for el in HaDeviceClass}
    doc_el = set(el.string for el in list_elements)
    missing = doc_el - known_el

    # None is special case, since it uses the python type None and not the string 'None'
    # See #4 and https://github.com/home-assistant/core/pull/85106
    if 'None' in missing:
        missing.remove('None')

    return missing


def parse_humidifier() -> set:
    """
    humidifier/dehumidifier doesn't have the normal docs.
    Check if the following strings are present:
    'humidifier', 'dehumidifier'
    :return: missing elements
    """
    required_el = set()
    required_el.add('humidifier')
    required_el.add('dehumidifier')
    known_el = {el.value for el in HaDeviceClass}
    missing = required_el - known_el
    return missing


def print_results(results: dict):
    """
    prints results of comparison of known values and values from docs
    :param results:
    :return:
    """
    for k, v in results.items():
        print(f"found {len(v)} missing items in category: {k}")
        print(50 * '=')

        for el in sorted(v):
            el = str(el)
            print(f"{el.upper()} = {repr(el)}")
        print("")


if __name__ == '__main__':
    complete = True
    missing_el = {}
    for k, v in urls.items():
        missing_el[k] = parse_url(v)
        if len(missing_el[k]) > 0:
            complete = False

    missing_el['humidifier'] = parse_humidifier()
    if len(missing_el['humidifier']) > 0:
        complete = False

    print_results(missing_el)

    if not complete:
        sys.exit(1)

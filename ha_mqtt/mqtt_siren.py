"""
this module contains code for the mqtt siren
"""
#  Copyright (c) 2024 - Andreas Philipp
#  This code is published under the MIT license

import json
import threading

from paho.mqtt.client import Client, MQTTMessage  # type: ignore

from . import util
from .mqtt_switch import MqttSwitch


class MqttSiren(MqttSwitch):
    """
    simple siren that runs a callback that can be used to
    play sounds or blink a light

    .. note::
       The on callback runs in a separate thread.
       Use locking mechanisms if required to prevent race conditions.

       The off callback runs synchronously.


    .. note::
       call `set_off()` in the end of your callback to automatically turn off the siren
       once the sound has been played
    """

    device_type = "siren"

    def pre_discovery(self) -> None:
        super().pre_discovery()
        self.remove_config_option('device_class')  # siren doesn't have a device class

    def command_callback(self, client: Client, userdata: object, msg: MQTTMessage) -> None:
        cmd_dict = json.loads(msg.payload.decode("ascii"))
        cmd_str = cmd_dict.get("state", util.OFF)
        if cmd_str.encode("ascii") == util.ON:
            self.set_on()
            threading.Thread(target=self.callback_on, name="callback_thread").start()
        else:
            self.set_off()
            self.callback_off()

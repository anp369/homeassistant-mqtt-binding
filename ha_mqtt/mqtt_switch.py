"""
this module contains all code for MQTT switches
"""
#  Copyright (c) 2024 - Andreas Philipp
#  This code is published under the MIT license

import threading

from paho.mqtt.client import Client, MQTTMessage  # type: ignore

from . import util
from .mqtt_device_base import MqttDeviceSettings, MqttDeviceBase
from .util import HaSwitchDeviceClass


class MqttSwitch(MqttDeviceBase):
    """
    MQTT Switch class.
    Implements a binary switch, that knows the states ON and OFF

    :param settings: As in :class:`~ha_mqtt.mqtt_device_base.MqttDeviceBase`
    :param device_class: device class of this switch

    Usage:
    assign custom functions to the `callback_on` and `callback_off` members.
    These functions get executed in a separate thread once the according payload was received

    .. attention::
       Each callback spawns a new thread which is automatically destroyed once the function finishes.
       Be aware of that if you do non threadsafe stuff in your callbacks
    """

    device_type = "switch"
    initial_state = util.OFF

    def __init__(self, settings: MqttDeviceSettings, device_class: HaSwitchDeviceClass = HaSwitchDeviceClass.SWITCH):
        # internal tracker of the state
        self.state: bool = self.__class__.initial_state != util.OFF

        self.device_class = device_class

        # callback executed when an on command is received via MQTT
        self.callback_on = lambda: None

        # callback executed when an on command is received via MQTT
        self.callback_off = lambda: None
        self.cmd_topic = ""

        super().__init__(settings)

    def stop(self) -> None:
        self._client.unsubscribe(self.cmd_topic)
        super().stop()

    def pre_discovery(self) -> None:
        self.cmd_topic = f"{self.base_topic}/set"
        self.add_config_option("device_class", self.device_class.value)
        self.add_config_option("command_topic", self.cmd_topic)
        self.add_config_option("payload_off", util.OFF.decode('ascii'))
        self.add_config_option("payload_on", util.ON.decode('ascii'))

        self._client.subscribe(self.cmd_topic)
        self._client.message_callback_add(self.cmd_topic, self.command_callback)

    def post_discovery(self) -> None:
        self.set_off()

    def set_on(self) -> None:
        """
        report to homeassistant, that the device is in 'on' state
        """
        self.state = True
        self.update_state(util.ON)

    def set_off(self) -> None:
        """
        report to homeassistant, that the device is in 'off' state
        """
        self.state = False
        self.update_state(util.OFF)

    def set(self, state: bool) -> None:
        """
        sets the switch to the given state
        :param state: state to set to
        """
        if state:
            self.set_on()
        else:
            self.set_off()

    def command_callback(self, client: Client, userdata: object, msg: MQTTMessage) -> None:  # pylint: disable=W0613
        """
        callback that is executed when a message on the *command* channel is received

        :param client: client who received the message
        :param userdata: user defined data of any type that is passed as the userdata parameter to callbacks.
          It may be updated at a later point with the user_data_set() function.
        :param msg: actual message sent

        """
        if msg.payload == util.ON:
            threading.Thread(target=self.callback_on, name="callback_thread").start()
        elif msg.payload == util.OFF:
            threading.Thread(target=self.callback_off, name="callback_thread").start()
        else:
            self._logger.warning("got invalid payload as command: %s", msg.payload)

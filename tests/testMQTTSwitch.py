#  Copyright (c) 2024 - Andreas Philipp
#  This code is published under the MIT license

import unittest
import unittest.mock as mock

from ha_mqtt import util
from ha_mqtt.mqtt_switch import MqttSwitch, MqttDeviceSettings


class TestMQTTSwitch(unittest.TestCase):

    def setUp(self) -> None:
        self.name = "Test"
        self.identifier = "test"
        self.settings = MqttDeviceSettings(self.name, self.identifier, None, None)

    @mock.patch('paho.mqtt.client.Client')
    def test_close(self, mocked_client):
        client = mocked_client('test')
        self.settings.client = client
        sw = MqttSwitch(self.settings, util.HaSwitchDeviceClass.SWITCH)
        sw.close()

        client.unsubscribe.assert_any_call(sw.cmd_topic)

    @mock.patch('paho.mqtt.client.Client')
    @mock.patch('paho.mqtt.client.MQTTMessage')
    def test_callback(self, mocked_client, mocked_message):
        client = mocked_client('test')
        self.settings.client = client
        callbacks = mock.Mock()

        sw = MqttSwitch(self.settings, util.HaSwitchDeviceClass.SWITCH)
        sw.callback_on = callbacks.cb_on
        sw.callback_off = callbacks.cb_off

        msg_on = mocked_message()
        msg_on.payload = util.ON
        sw.command_callback(None, None, msg_on)
        callbacks.cb_on.assert_called_once()

        msg_off = mocked_message()
        msg_off.payload = util.OFF
        sw.command_callback(None, None, msg_off)
        callbacks.cb_off.assert_called_once()

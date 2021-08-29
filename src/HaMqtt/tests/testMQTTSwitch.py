import unittest
import unittest.mock as mock

from src.HaMqtt import MQTTUtil
from src.HaMqtt.MQTTSwitch import MQTTSwitch


class TestMQTTSwitch(unittest.TestCase):

    def setUp(self) -> None:
        self.name = "Test"
        self.identifier = "test"

    @mock.patch('paho.mqtt.client.Client')
    def test_close(self, mocked_client):
        client = mocked_client('test')

        sw = MQTTSwitch(self.name, self.identifier, client)
        sw.close()

        client.unsubscribe.assert_any_call(sw.cmd_topic)

    @mock.patch('paho.mqtt.client.Client')
    @mock.patch('paho.mqtt.client.MQTTMessage')
    def test_callback(self, mocked_client, mocked_message):
        client = mocked_client('test')
        callbacks = mock.Mock()

        sw = MQTTSwitch(self.name, self.identifier, client)
        sw.callback_on = callbacks.cb_on
        sw.callback_off = callbacks.cb_off

        msg_on = mocked_message()
        msg_on.payload = MQTTUtil.ON
        sw.command_callback(None, None, msg_on)
        callbacks.cb_on.assert_called_once()

        msg_off = mocked_message()
        msg_off.payload = MQTTUtil.OFF
        sw.command_callback(None, None, msg_off)
        callbacks.cb_off.assert_called_once()

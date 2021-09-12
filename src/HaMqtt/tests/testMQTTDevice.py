import json
import unittest
import unittest.mock as mock

from src.HaMqtt.MQTTDevice import MQTTDevice


class TestMQTTDevice(unittest.TestCase):

    @mock.patch('paho.mqtt.client.Client')
    def test_initialize(self, mocked_client):
        client = mocked_client('test')

        name = "Test Device"
        identifier = "test"
        unique_id = "abcdefg"

        dev = MQTTDevice(name, identifier, client, False, unique_id=unique_id)

        self.assertEqual(name, dev.name)
        self.assertEqual(identifier, dev.node_id)
        self.assertEqual(f"{MQTTDevice.base_topic}/sensor/{identifier}", dev.base_topic)
        self.assertEqual(f"{MQTTDevice.base_topic}/sensor/{identifier}/available", dev.avail_topic)
        self.assertEqual(f"{MQTTDevice.base_topic}/sensor/{identifier}/config", dev.config_topic)
        self.assertEqual(f"{MQTTDevice.base_topic}/sensor/{identifier}/state", dev.state_topic)
        self.assertTrue(dev.conf_dict)
        self.assertEqual("abcdefg", dev._unique_id)
        self.assertEqual(dev.conf_dict['unique_id'], unique_id)
        client.subscribe.assert_called_with(dev.state_topic)
        client.publish.assert_any_call(dev.config_topic, json.dumps(dev.conf_dict), retain=True)
        client.publish.assert_any_call(dev.avail_topic, 'online', qos=1, retain=True)

    @mock.patch('paho.mqtt.client.Client')
    def test_deletion(self, mocked_client):
        client = mocked_client('test')
        name = "Test Device"
        identifier = "test"

        dev = MQTTDevice(name, identifier, client, False)
        topic = dev.avail_topic
        dev.close()

        client.publish.assert_any_call(topic, 'offline', qos=1, retain=True)

    @mock.patch('paho.mqtt.client.Client')
    def test_online(self, mocked_client):
        client = mocked_client('test')
        name = "Test Device"
        identifier = "test"

        dev = MQTTDevice(name, identifier, client, False)
        topic = dev.state_topic

        dev.send_online()
        client.publish.called_with(topic, 'online', qos=1, retain=True)

        dev.send_offline()
        client.publish.called_with(topic, 'offline', qos=1, retain=True)

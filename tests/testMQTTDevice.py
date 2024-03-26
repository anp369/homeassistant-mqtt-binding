#  Copyright (c) 2024 - Andreas Philipp
#  This code is published under the MIT license

import json
import unittest
import unittest.mock as mock

from ha_mqtt.ha_device import HaDevice
from ha_mqtt.mqtt_device_base import MqttDeviceBase, MqttDeviceSettings
from ha_mqtt.util import EntityCategory


class TestMQTTDevice(unittest.TestCase):
    def setUp(self) -> None:
        self.settings = MqttDeviceSettings("test", "abcdefg", None, None)

        self.name = "test"
        self.unique_id = "abcdefg"

    @mock.patch('paho.mqtt.client.Client')
    def test_initialize(self, mocked_client):
        client = mocked_client('test')
        self.settings.client = client

        dev = MqttDeviceBase(self.settings, False)
        dev.start()

        self.assertEqual(self.name, dev.name)
        self.assertEqual(self.unique_id, dev._unique_id)
        self.assertEqual(f"{MqttDeviceBase.base_topic}/sensor/{self.unique_id}", dev.base_topic)
        self.assertEqual(f"{MqttDeviceBase.base_topic}/sensor/{self.unique_id}/available", dev.avail_topic)
        self.assertEqual(f"{MqttDeviceBase.base_topic}/sensor/{self.unique_id}/config", dev.config_topic)
        self.assertEqual(f"{MqttDeviceBase.base_topic}/sensor/{self.unique_id}/state", dev.state_topic)
        self.assertTrue(dev._conf_dict)
        self.assertEqual("abcdefg", dev._unique_id)
        self.assertEqual(dev._conf_dict['unique_id'], self.unique_id)
        client.subscribe.assert_called_with(dev.state_topic)
        client.publish.assert_any_call(dev.config_topic, json.dumps(dev._conf_dict), retain=True)
        client.publish.assert_any_call(dev.avail_topic, 'online', qos=1, retain=True)

    @mock.patch('paho.mqtt.client.Client')
    def test_offline(self, mocked_client):
        client = mocked_client('test')
        self.settings.client = client

        dev = MqttDeviceBase(self.settings, False)
        topic = dev.avail_topic
        dev.stop()

        client.publish.assert_any_call(topic, 'offline', qos=1, retain=True)

    @mock.patch('paho.mqtt.client.Client')
    def test_online(self, mocked_client):
        client = mocked_client('test')
        self.settings.client = client

        dev = MqttDeviceBase(self.settings, False)
        topic = dev.state_topic

        dev.set_online()
        client.publish.called_with(topic, 'online', qos=1, retain=True)

        dev.set_offline()
        client.publish.called_with(topic, 'offline', qos=1, retain=True)

    @mock.patch('paho.mqtt.client.Client')
    def test_device_mapping(self, mocked_client):
        client = mocked_client('test')
        device = HaDevice("Device1", "abcxyz")
        self.settings = MqttDeviceSettings("device_test_entity", "abcefghi", client, device)

        dev = MqttDeviceBase(self.settings, False)
        self.assertTrue(dev._conf_dict['device'] == self.settings.device.get_dict())

    @mock.patch('paho.mqtt.client.Client')
    def test_entity_category(self, mocked_client):
        client = mocked_client("test")
        device = HaDevice("Device1", "abcxyz")
        self.settings = MqttDeviceSettings("ent_category_test", "extremly_unique_aaa", client, device,
                                           EntityCategory.CONFIG)
        entity = MqttDeviceBase(self.settings, False)
        self.assertEqual("config", entity._conf_dict["entity_category"])

        # make sure if category is primary, the option is completely omitted from the config dict
        self.settings = MqttDeviceSettings("ent_category_test", "extremly_unique_aaa", client, device,
                                           EntityCategory.PRIMARY)
        entity2 = MqttDeviceBase(self.settings, False)
        self.assertNotIn("entity_category", entity2._conf_dict)

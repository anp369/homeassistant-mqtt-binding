import json
import logging
import time
import uuid

from paho.mqtt.client import Client, MQTTMessage


class MQTTDevice:
    """
    base class for homeassistant mqtt devices.
    handles:
      - availability topic
      - discovery
      - setting base settings
    """

    base_topic = "homeassistant"
    device_type = "sensor"
    initial_state = 0

    @classmethod
    def set_basetopic(cls, topic: str) -> None:
        """
        sets the basetopic for the application to publish all other topics under,
        for example 'homeassistant'. Call this function before instantiating child objects
        :param topic: the topic to use
        :return:
        """
        MQTTDevice.base_topic = topic

    def __init__(self, name: str, node_id: str, client: Client, send_only=False, unique_id=str(uuid.uuid4())):
        """
        initializes the mqtt device instance. Make sure to add more configuration in base_classes,
        as this class itself can't be used
        :param name: Friendly name of the device to be shown in homeassistant
        :param node_id: node id used for assigning an mqtt topic to the node
        :param client: paho mqtt client instance
        :param send_only: set this to True, if this Device only sends data to the broker, to
        :param unique_id: unique id to identify this device against homeassistant
        disable all parts that subscribe to topics etc.
        """
        self.name = name
        self.node_id = node_id
        self.send_only = send_only
        self._client = client
        assert type(unique_id) == str, "the unique ID must be a string"
        self._unique_id = unique_id

        self._logger = logging.getLogger(node_id)

        self.base_topic = f"{self.__class__.base_topic}/{self.__class__.device_type}/{self.node_id}"
        self.avail_topic = f"{self.base_topic}/available"
        self.config_topic = f"{self.base_topic}/config"
        self.state_topic = f"{self.base_topic}/state"

        self.conf_dict = {
            'name': self.name,
            'state_topic': self.state_topic,
            'availability_topic': self.avail_topic,
            'unique_id': unique_id
        }

        if not send_only:
            self._client.subscribe(self.state_topic)
            self._client.message_callback_add(self.state_topic, self.state_callback)

        self.initialize()

        self._send_discovery()

    def close(self):
        """
        sets itself as offline and unsubscribes from all topic regarding this instance
        :return:
        """
        self.send_offline()
        self._client.unsubscribe(f"{self.base_topic}/#")  # unsubscribe from all topics

    def add_config_option(self, key: str, value: str):
        """
        add parameter to the configuration dictionary sent during discovery
        :param key: key of the option
        :param value: value of the option
        :return:
        """
        self.conf_dict[key] = value

    def initialize(self):
        """
        run additional tasks before sending out the discovery command
        useful in subclasses that add additional configuration parameters
        :return:
        """
        pass

    def publish_state(self, payload):
        """
        publishes a payload on the state topic
        :param payload: payload to publish
        :return:
        """
        self._client.publish(self.state_topic, payload, retain=True)

    def state_callback(self, client: Client, userdata, msg: MQTTMessage):
        """
        callback that gets executed when receiving a message on the state topic
        :param client:
        :param userdata:
        :param msg:
        :return:
        """
        pass

    def send_online(self):
        """
        send the available payload on the available channel
        :return:
        """
        self._client.publish(self.avail_topic, 'online', qos=1, retain=True)

    def send_offline(self):
        """
        send the unavailable payload on the available channel
        :return:
        """
        self._client.publish(self.avail_topic, 'offline', qos=1, retain=True)

    def delete_config(self):
        """
        delete the sensor from homeassistant,
        sends an empty payload to the config topic
        :return:
        """
        self._client.publish(self.config_topic, "")

    def _send_discovery(self, send_initial=True):
        """
        sends discovery package to broker
        :param send_initial: determines if the classes' initital state should be sent or not
        :return:
        """
        self._client.publish(self.config_topic, json.dumps(self.conf_dict), retain=True)
        time.sleep(0.01)
        self.send_online()
        self._logger.debug(f"sending config for {self.node_id}: {self.conf_dict}")
        if send_initial:
            self.publish_state(self.__class__.initial_state)

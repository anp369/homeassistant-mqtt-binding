"""
this module contains the MqttDeviceBase, a baseclass for all other mqtt devices
"""

#  Copyright (c) 2024 - Andreas Philipp
#  This code is published under the MIT license

import json
import logging
import time
from dataclasses import dataclass
from typing import Any, Dict, Optional, Union

from paho.mqtt.client import Client, MQTTMessage  # type: ignore

from .ha_device import HaDevice
from .util import EntityCategory


@dataclass
class MqttDeviceSettings:
    """
    class for storing settings like name and unique ID

    :param name: Friendly name of the device to be shown in homeassistant
    :param unique_id: unique id to identify this device against homeassistant
    :param client: paho mqtt client instance
    :param device: :class:`~ha_mqtt.ha_device.HaDevice`, to group multiple entities together
    :param entity_type: :class:`~ha_mqtt.util.EntityCategory` Category of the entity
    :param will_topic: the already set will on the client. Will be passed to HA to check if dev is still online
    """

    def __init__(
            self,
            name: str,
            unique_id: str,
            client: Client,
            device: Optional[HaDevice] = None,
            entity_type: EntityCategory = EntityCategory.PRIMARY,
            will_topic: str = ""
    ):
        assert isinstance(unique_id, str), "the unique ID must be a string"
        self.device = device
        self.name = name
        self.unique_id = unique_id
        self.client = client
        self.entity_type = entity_type
        self.will_topic = will_topic


class MqttDeviceBase:
    """
    base class for homeassistant mqtt devices.
    handles:

    - availability topic
    - discovery
    - setting base settings

    when setting `send_only` to True no subscriptions are made, and the device is configured to just
    send values to the broker, which makes it useable for small sensors, that just report values to the broker
    but not actually receive any commands


    :param send_only: set this to True, if this Device only sends data to the broker, for example a simple sensor, to
        disable all parts that subscribe to topics etc.

    :param settings: settings object containing the basic  information of the entity. See
        :class:`~ha_mqtt.mqtt_device_base.MqttDeviceSettings` for additional info

    .. note::
       this is the base class all other devices inherit from.

    .. important::
       make sure that unique_id is really **really** unique, as it is used by the
       homeassistant internals to differentiate between the devices. Some strange things may happen
       if IDs aren't unique. One possibility would be using uuid.uuid4() or pulling them
       out of config file.

    """

    base_topic = "homeassistant"
    """
    mqtt basetopic that is used as parent for all nodes this device produces
    """

    device_type = "sensor"
    """
    string that is used to group the mqtt topics to
    for example {basetopic}/{device_type}/id/state
    use 'sensor' for sensors, 'switch' for switches etc.

    .. note::
       see https://www.home-assistant.io/docs/mqtt/discovery/ for more info
    """

    send_initial = False
    """
    If set to true, initial state will be sent during discovery
    """

    _initial_state = 0

    @classmethod
    def set_basetopic(cls, topic: str) -> None:
        """
        sets the basetopic for the application to publish all other topics under,
        for example 'homeassistant'. Call this function before instantiating child objects
        :param topic: the topic to use
        """
        MqttDeviceBase.base_topic = topic

    def __init__(self, settings: MqttDeviceSettings, send_only: bool = False):
        """
        initializes the mqtt device instance. Make sure to add more configuration in base_classes,
        as this class itself can't be used
        """
        self.name = settings.name
        self.send_only = send_only
        self._client = settings.client
        self._unique_id = settings.unique_id
        self._entity_type = settings.entity_type
        self._will_topic = settings.will_topic

        self._logger = logging.getLogger(self.name)
        self._started = False

        self.base_topic = f"{self.__class__.base_topic}/{self.__class__.device_type}/{self._unique_id}"
        self.avail_topic = f"{self.base_topic}/available"
        self.config_topic = f"{self.base_topic}/config"
        self.state_topic = f"{self.base_topic}/state"

        self._conf_dict: Dict[str, Any] = {}

        self.add_config_option('name', self.name)
        self.add_config_option('state_topic', self.state_topic)
        self.add_config_option('unique_id', self._unique_id)

        # if a will is supplied, specify both the client will and the
        # availability topic as availability
        if self._will_topic:
            self.add_config_option('availability', [
                {'topic': self.avail_topic},
                {'topic': self._will_topic}
            ])
            # make sure both topics show online to show the device as online
            self.add_config_option('availability_mode', 'all')
        else:
            self.add_config_option('availability_topic', self.avail_topic)

        # set entity category
        if self._entity_type != EntityCategory.PRIMARY:
            self._conf_dict["entity_category"] = self._entity_type.value

        # set device configuration if specified
        if settings.device is not None:
            assert len(settings.device.identifiers) > 0, \
                "You must set one of identifiers or connections." \
                " See https://www.home-assistant.io/integrations/sensor.mqtt/#device for more info"
            self._conf_dict['device'] = settings.device.get_dict()

    @property
    def is_started(self) -> bool:
        """
        :return: True, if the device has started and communication with the broker is done
        """
        return self._started

    def start(self) -> None:
        """
        subscribes to all topics, runs discovery and publishes initial state info

        .. note::
           run this after connecting to the broker

        """
        if not self.send_only:
            self._client.subscribe(self.state_topic)

        self._client.message_callback_add(
            self.state_topic, self.state_callback)

        # run discovery process
        self.pre_discovery()
        self._send_discovery(self.send_initial)
        self._started = True
        self.post_discovery()

    def stop(self) -> None:
        """
        sets itself as offline and unsubscribes from all topic regarding this instance

        .. attention::
           call this when closing or destructing your application to do proper cleanup
        """
        self._started = False
        self.set_offline()
        # unsubscribe from all topics
        self._client.unsubscribe(f"{self.base_topic}/#")

    def add_config_option(self, key: str, value: Union[str, dict, list]) -> None:
        """
        add parameter to the configuration sent during discovery.
        Use this in child classes to add any additional configuration necessary for the device to work
        :param key: str - key of the option
        :param value: value of the option, must be json serializable

        .. important::
           call this in the `pre_discovery()` method of child classes.
           Otherwise, the discovery package gets sent out before the parameters could be registered,
           leading to a faulty configuration
        """
        self._conf_dict[key] = value

    def remove_config_option(self, key: str) -> None:
        """
        removes the given config option from this device
        :param key: option to remove
        """
        self._conf_dict.pop(key)

    def pre_discovery(self) -> None:
        """
        run additional tasks before sending out the discovery command.
        useful in subclasses that add additional configuration parameters
        Override this in subclasses for additional initialization before discovery
        Runs synchronously.
        """

    def post_discovery(self) -> None:
        """
        run additional tasks after sending out the discovery command
        Useful in subclasses to run initialization of internal values
        Runs synchronously.
        """

    def update_state(
            self,
            payload: Union[str, bytes, bytearray, int, float, None],
            retain: bool = True,
    ) -> None:
        """
        publishes a payload on the device's state topic,
        updating its state in homeassistant

        :param payload: payload to publish
        :param retain: set to True to send as a retained message
        """

        self._logger.debug("publishing payload '%s' for %s", payload, self._unique_id)

        self._client.publish(self.state_topic, payload, retain=retain)
        time.sleep(0.01)

    def state_callback(self, client: Client, userdata: object, msg: MQTTMessage) -> None:
        """
        callback that gets executed when receiving a message on the state topic
        Override this in subclasses to trigger actions when messages are received

        :param client: the paho MQTT client that received the message
        :param userdata: user defined data of any type that is passed as the userdata parameter to callbacks.
                         It may be updated at a later point with the user_data_set() function.
        :param msg: the actual message containing the payload
        """

    def set_online(self) -> None:
        """
        report this device as online to homeassistant.
        send the available payload on the available channel
        """
        self._client.publish(self.avail_topic, 'online', qos=1, retain=True)

    def set_offline(self) -> None:
        """
        report this device as offline to homeasstiant
        send the unavailable payload on the available channel
        """
        self._client.publish(self.avail_topic, 'offline', qos=1, retain=True)

    def delete(self) -> None:
        """
        delete the sensor from homeassistant
        by sending an empty payload to the config topic
        """
        self._client.publish(self.config_topic, "")

    def _send_discovery(self, send_initial: bool = True) -> None:
        """
        sends discovery package to broker

        :param send_initial: determines if the classes' initital state should be sent or not
        """
        self._client.publish(self.config_topic, json.dumps(
            self._conf_dict), retain=True)
        time.sleep(0.01)
        self.set_online()
        self._logger.debug("sending config for %s: %s",
                           self._unique_id, self._conf_dict)
        if self._will_topic:
            self._client.publish(self._will_topic, 'online', retain=True)

        if send_initial:
            self.update_state(
                self.__class__._initial_state)  # pylint: disable=W0212

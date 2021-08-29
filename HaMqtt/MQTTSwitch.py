import uuid

from paho.mqtt.client import Client

from . import MQTTDevice, MQTTUtil


class MQTTSwitch(MQTTDevice.MQTTDevice):
    device_type = "switch"
    initial_state = MQTTUtil.OFF

    def __init__(self, name: str, node_id: str, client: Client, unique_id: str = str(uuid.uuid4())):
        # internal tracker of the state
        self.state = self.__class__.initial_state

        # callback executed when an on command is recevied via MQTT
        self.callback_on = lambda: None

        # callback executed when an on command is received via MQTT
        self.callback_off = lambda: None
        self.cmd_topic = ""

        super().__init__(name, node_id, client, unique_id=unique_id)

    def close(self):
        """
        sends offline message and unsubscribes from all topics regarding this instance
        :return:
        """
        self._client.unsubscribe(self.cmd_topic)
        super(MQTTSwitch, self).close()

    def initialize(self):
        """
        run stuff before the discovery is sent
        :return:
        """
        self.cmd_topic = f"{self.base_topic}/set"
        self.add_config_option("command_topic", self.cmd_topic)
        self.add_config_option("payload_off", 'off')
        self.add_config_option("payload_on", 'on')

        if not self.send_only:
            self._client.subscribe(self.cmd_topic)
            self._client.message_callback_add(self.cmd_topic, self.command_callback)

    def set_on(self):
        """
        sends to the broker, that the device is in 'on' state
        :return:
        """
        self.state = True
        self.publish_state(MQTTUtil.ON)

    def set_off(self):
        """
        sends to the broker, that the device is in 'off' state
        :return:
        """
        self.state = False
        self.publish_state(MQTTUtil.OFF)

    def set(self, state: bool):
        """
        sets the switch to the given state
        :param state: state to set to
        :return:
        """
        if state:
            self.set_on()
        else:
            self.set_off()

    def command_callback(self, client, userdata, msg):
        """
        callback that is executed when a message on the command channel is received
        :param client: client who received the message
        :param userdata: attached userdata
        :param msg: actual message sent
        :return:
        """
        if msg.payload == MQTTUtil.ON:
            self.callback_on()
        elif msg.payload == MQTTUtil.OFF:
            self.callback_off()
        else:
            self._logger.warn(f"got invalid payload as command: {msg.payload}")

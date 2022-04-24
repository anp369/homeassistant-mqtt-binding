import json
import threading
import uuid

from paho.mqtt.client import Client

from . import MQTTUtil
from .MQTTSwitch import MQTTSwitch


class MQTTSiren(MQTTSwitch):
    device_type = "siren"

    def __init__(self, name: str, node_id: str, client: Client, unique_id=str(uuid.uuid4())):
        super().__init__(name, node_id, client, unique_id=unique_id)

    def command_callback(self, client, userdata, msg):
        cmd_dict = json.loads(msg.payload.decode("ascii"))
        cmd_str = cmd_dict.get("state", MQTTUtil.OFF)
        if cmd_str.encode("ascii") == MQTTUtil.ON:
            self.set_on()
            threading.Thread(target=self.callback_on, name="callback_thread").start()
        else:
            self.set_off()
            self.callback_off()

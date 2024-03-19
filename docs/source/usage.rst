=====
Usage
=====

General usage
=============
.. hint::
  see the ``examples/`` folder for excutable code, that shows how implement
  the devices.

Choose the appropriate device.
Some Sensors such as thermometers are already implemented.
All other sensors may work by settings the correct type.
See ``ha_mqtt/util.py`` for all defined devices.

#. create an ``paho mqtt`` client instance and connect it to your broker.

#. supply all necessary callbacks.
   For switches this would be ``callback_on()`` and ``callback_off()``
#. Instantiate your device

#. make sure to run the  ``close()`` method before deleting your object.


Using will topics
=================
As stated in the `paho documentation <https://eclipse.dev/paho/files/paho.mqtt.python/html/client.html#paho.mqtt.client.Client.will_set>`_,
the will must be set before connecting the client.
As this library has no effect on when the client actually connects, the
user must make the ``will_set()`` call accordingly.

#. set the will in the ``Client`` object with ``will_set()``. Set ``retain=True``
#. specify the will topic in :class:`~ha_mqtt.mqtt_device_base.MqttDeviceSettings`
#. connect to the broker
#. run initialization on the MQTT Devices

.. warning::
  If you're using strict ACLs on your broker, make sure that homeassistant is allowed
  ro read the will topic. Otherwise availability detection might not work properly.


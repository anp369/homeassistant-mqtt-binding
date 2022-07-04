Usage
=====

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
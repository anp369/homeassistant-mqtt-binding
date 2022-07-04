Installation
==============

1. Download the package from pip using your
   favorite package manager
   pip: ``python -m pip install homeassistant-mqtt-binding``
2. Run a MQTT server such as `mosquitto`_
3. Add the homeassistant MQTT integration if not done yet and configure it
   to use the mqtt server. Make sure to leave the prefix to ``homeassistant``
   Details can be found here: `homeassistant mqtt docs`_

.. _mosquitto: https://mosquitto.org/
.. _homeassistant mqtt docs: https://www.home-assistant.io/integrations/mqtt/
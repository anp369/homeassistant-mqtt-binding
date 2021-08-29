# Homeassistant MQTT Binding for python

This package enables you to implement arbitrary devices in python supported in homeassistant. The communication with
homeassistant is handled by MQTT. For example you could write an simple program running on a raspberry pi controlling an
LED. By exposing this configuration to homeassistant you can easily control the LED via HA.

The base class handles the following things automatically:

* registering devices in homeassistant through the mqtt discovery protocol
* setting the device as available once fully setup
* setting the device unavailable when quitting the application

### Installation

`python3 -m pip install homeassistant-mqtt-binding`
the dependencies should be installed automatically

### Usage

1. create an paho mqtt Client instance connected to your mqtt server
2. instantiate your desired device and pass the Client instance to the constructor
3. when your program closes make sure to call the `close()` function of each device for cleanup

### Examples

The following examples require an already running stack of homeassistant and an MQTT server.  
See the [examples](https://gitlab.com/anphi/homeassistant-mqtt-binding/HaMqtt/examples) folder for all demo scripts.

* switch.py:
  simple switch device that can be toggled by homeassistant

### Expanding the application

Since I don't use all devices I haven't implemented them yet. You can easily implement any missing device:

1. create an empty class subclassing any of the devices (normally you would subclass `MQTTDevice` or `MQTTSensor`).
2. implement the `initialize()` function. It gets called in the parent constructor right before it sends out the
   discovery payload to the broker. Use `add_config_option()` to add your own settings to the configuration dictionary.
3. Implement any callbacks that might be necessary for all devices that can receive data. (commands for switches for
   example).
4. If your device needs more topics than state, configuration and set, feel free to implement them
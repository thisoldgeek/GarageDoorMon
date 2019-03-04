# **GarageDoorMon**

 
## *Description:*
An Adafruit Feather Huzzah that posts garage door open/closed status to adafruit.io.
The adafruit.io MQTT feed is subscribed to by a raspberry pi zero w and the status
(SHUT/OPEN) is displayed on a 4-digit alphanumeric display connected to the pi zero w.

This is basically the project from: https://learn.adafruit.com/using-ifttt-with-adafruit-io/overview,
with a few tweaks and add-ons:
* GarageDoorMon doesn't use a battery, it's powered by a 5V adapter; requires mains power source, long wire
* Logic is reversed, a '1' is sent to adafruit.io when the garage door is open, '0' when closed(SHUT)
* Added: raspberry pi zero w runs a system service to monitor the door status, shows on 4-digit display
* IFTTT is not required! Of course, you can use it if you like. 
This version uses MQTT subscribe directly from adafruit.io feed, via python cllient code.

See the posting at:

thisoldgeek.blogspot.com Garage Door Monitor

## *Required Software:*
Requires install of the library from: https://github.com/adafruit/Adafruit_Python_LED_Backpack
See the README on that git for instructions

Also requires sign-up/set-up for adafruit.io; follow the instructions in:
https://learn.adafruit.com/using-ifttt-with-adafruit-io/adafruit-io-setup-uniontownlabs

If you use this MQTT version, follow the instructions to install the adafruit.io python client library:
https://learn.adafruit.com/welcome-to-adafruit-io/client-library

Also - review the MQTT documentation:
https://learn.adafruit.com/welcome-to-adafruit-io/mqtt-api-documentation-2

Bonus: Modified mosquitto.conf. Use this to set up bridging from adafruit.io to a local MQTT broker. 
This is useful if you already have a your own broker.


## *Required Hardware:*
* Adafruit Feather Huzzah
* Wire - used 18 AWG thermostat wire
* Magnetic Door Switch, Normally Open (NO)
* External resistor pullup network
* Adafruit 4 digit 14-segment alphanumeric display, for status
* Raspberry Pi Zero W

## *Fabrication:*
* Optional Adafruit Feather Huzzah 3D printed case; M2 screws (https://www.thingiverse.com/thing:2209964)
* Optional Adafruit 3D printed case for raspberry pi zero W (https://www.thingiverse.com/thing:1165227)
* Double-side foam tape to fasten alphanumeric display to raspberry pi case

#!/usr/bin/env python3

# Example of using the MQTT client class to subscribe to and publish feed values.
# Author: Tony DiCola

# Import standard python modules.
import random
import sys
import time
import datetime
import RPi.GPIO as GPIO

#Select GPIO mode
GPIO.setmode(GPIO.BCM)
#Set buzzer - pin 17 as output
buzzer=17
GPIO.setup(buzzer,GPIO.OUT)
GPIO.output(buzzer,GPIO.LOW)  # Set buzzer off to start

alert = 0 # If =1 then buzzer function

# Import Adafruit IO MQTT client.
from Adafruit_IO import MQTTClient

from Adafruit_LED_Backpack import AlphaNum4

# Create display instance on default I2C address (0x70) and bus number.
display = AlphaNum4.AlphaNum4()

# Initialize the display. Must be called once before using the display.
display.begin()
display.set_brightness(2)

myText =  "STRT"

# Set to your Adafruit IO key.
# Remember, your key is a secret,
# so make sure not to publish it when you publish this code!
ADAFRUIT_IO_KEY = '********************************'
# Set to your Adafruit IO username.
# (go to https://accounts.adafruit.com to find your username)
ADAFRUIT_IO_USERNAME = '**********'

# Quiet Time: no alert actions will take place
quiet_start = 21			# quiet time starts at this hour, using 24hr style
quiet_end = 9				# quiet time ends at this hour

# DO NOT CHANGE program variable default that follows: quiet_state
# Program toggles to indicate if alerts will activate ("True") or be quiet ("False")
# This assumes you are running this program BEFORE quiet_start time
quiet_state = False

def quiet_time():
    #global quiet_start	# start time for quiet	
    #global quiet_end	# end time for quiet
    global quiet_state	# quiet True/False
	
    now = datetime.datetime.now()
    print(now)
    t = now.hour	# will be in 24hr format
		
    if quiet_state is False:
        if t >= quiet_start:
           quiet_state = True

        if quiet_state is True and t <= 12:
           if t >= quiet_end:
              quiet_state = False 

    return(quiet_state)


def beep():
    global alert
    global buzzer

    for i in range(3):
        GPIO.output(buzzer,GPIO.HIGH)
        #print ("Beep")
        time.sleep(0.5) # Delay in seconds
        GPIO.output(buzzer,GPIO.LOW)
        #print ("No Beep")
        time.sleep(0.5)
    alert = 0

# Define callback functions which will be called when certain events happen.
def connected(client):
    # Connected function will be called when the client is connected to Adafruit IO.
    # This is a good place to subscribe to feed changes.  The client parameter
    # passed to this function is the Adafruit IO MQTT client so you can make
    # calls against it easily.
    print('Connected to Adafruit IO!  Listening for GarageDoor changes...')
    # Subscribe to changes on a feed named DemoFeed.
    client.subscribe('GarageDoor')

def disconnected(client):
    # Disconnected function will be called when the client disconnects.
    print('Disconnected from Adafruit IO!')
    sys.exit(1)

def message(client, feed_id, payload):
    global myText
    # Message function will be called when a subscribed feed has a new value.
    # The feed_id parameter identifies the feed, and the payload parameter has
    # the new value.
    print('Feed {0} received new value: {1}'.format(feed_id, payload))
    # if payload == '1':
    #   myText = "OPEN"
    #elif payload == '0':
    #   myText = "SHUT"
    
    myText = payload;

# Create an MQTT client instance.
client = MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

# Setup the callback functions defined above.
client.on_connect    = connected
client.on_disconnect = disconnected
client.on_message    = message

# Connect to the Adafruit IO server.
client.connect()

# Now the program needs to use a client loop function to ensure messages are
# sent and received.  There are a few options for driving the message loop,
# depending on what your program needs to do.

# The first option is to run a thread in the background so you can continue
# doing things in your program.
client.loop_background()

pos = 0

# Now send new values every 10 seconds.
print('Publishing a new message every 10 seconds (press Ctrl-C to quit)...')
while True:
    #value = random.randint(0, 100)
    #print('Publishing {0} to DemoFeed.'.format(value))
    #client.publish('GarageDoor', value)
    # Clear the display buffer.
    display.clear()
    # Print a 4 character string to the display buffer.
    display.print_str(myText[pos:pos+4])
    # Write the display buffer to the hardware.  This must be called to
    # update the actual display LEDs.
    display.write_display()
    # Increment position. Wrap back to 0 when the end is reached.
    pos += 1
    if pos > len(myText)-4:
        pos = 0
    if myText == "SHUT":
       alert = 1
    if myText == "OPEN" and alert == 1:
       if quiet_time() == False:
            beep()
    time.sleep(10)

# Another option is to pump the message loop yourself by periodically calling
# the client loop function.  Notice how the loop below changes to call loop
# continuously while still sending a new message every 10 seconds.  This is a
# good option if you don't want to or can't have a thread pumping the message
# loop in the background.
#last = 0
#print('Publishing a new message every 10 seconds (press Ctrl-C to quit)...')
#while True:
#   # Explicitly pump the message loop.
#   client.loop()
#   # Send a new message every 10 seconds.
#   if (time.time() - last) >= 10.0:
#       value = random.randint(0, 100)
#       print('Publishing {0} to DemoFeed.'.format(value))
#       client.publish('DemoFeed', value)
#       last = time.time()

# The last option is to just call loop_blocking.  This will run a message loop
# forever, so your program will not get past the loop_blocking call.  This is
# good for simple programs which only listen to events.  For more complex programs
# you probably need to have a background thread loop or explicit message loop like
# the two previous examples above.
#client.loop_blocking()

